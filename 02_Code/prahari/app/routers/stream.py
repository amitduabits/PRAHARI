from __future__ import annotations

from pathlib import Path

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse, PlainTextResponse, Response

from app import store
from app.auth import User, assert_write, require_user, verify_stream_token
from app.paths import resolve_media_path
from app.services import sessions

router = APIRouter()


@router.post("/api/sessions")
def open_session(body: dict, user: User = Depends(require_user)) -> dict:
    assert_write(user)
    camera_id = body.get("camera_id")
    cam = store.get_camera(camera_id)
    if not cam:
        raise HTTPException(status_code=404, detail="unknown camera")
    try:
        return sessions.start(cam)
    except RuntimeError as exc:
        raise HTTPException(status_code=429, detail=str(exc))


@router.get("/api/sessions")
def list_sessions(user: User = Depends(require_user)) -> dict:
    return {"open": sessions.active()}


@router.delete("/api/sessions/{camera_id}")
def close_session(camera_id: str, user: User = Depends(require_user)) -> dict:
    assert_write(user)
    sessions.stop(camera_id)
    return {"closed": camera_id}


@router.get("/api/stream/{camera_id}")
async def stream(camera_id: str, token: str = Query(...)) -> Response:
    verify_stream_token(token, camera_id)
    cam = store.get_camera(camera_id)
    if not cam:
        raise HTTPException(status_code=404, detail="unknown camera")
    protocol = (cam.get("protocol") or "").lower()
    if protocol == "file":
        path = resolve_media_path(cam.get("url") or "")
        if not path.is_file():
            raise HTTPException(
                status_code=404,
                detail="Drop own_feed.mp4 into 03_Data/recordings",
            )
        return FileResponse(path, media_type="video/mp4")
    sess = sessions.get(camera_id)
    if sess and sess.get("kind") == "ffmpeg":
        playlist = Path(sess["dir"]) / "index.m3u8"
        if playlist.is_file():
            return FileResponse(playlist, media_type="application/vnd.apple.mpegurl")
        raise HTTPException(status_code=503, detail="ffmpeg session warming up")
    if cam.get("hls"):
        async with httpx.AsyncClient(timeout=10.0) as client:
            upstream = await client.get(cam["hls"])
        text = upstream.text
        return PlainTextResponse(text, media_type="application/vnd.apple.mpegurl")
    if not sess:
        raise HTTPException(status_code=503, detail="open a session first")
    raise HTTPException(status_code=503, detail="rtsp remux unavailable; install ffmpeg or use HLS")
