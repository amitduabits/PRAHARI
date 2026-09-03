from __future__ import annotations

import re
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse, PlainTextResponse, Response

from app import store
from app.auth import User, assert_write, require_user, verify_stream_token
from app.paths import resolve_media_path
from app.services import sessions
from app.services.catalogue import origin_get

router = APIRouter()

_HLS_PART = re.compile(r"^[\w.\-]+$")


def _rewrite_playlist(text: str, camera_id: str, token: str) -> str:
    prefix = f"/api/stream/{camera_id}/hls/"
    suffix = f"?token={token}"
    out: list[str] = []
    for line in text.splitlines():
        if line.startswith("#EXT-X-KEY:"):
            line = re.sub(r'URI="[^"]+"', f'URI="{prefix}enc.key{suffix}"', line)
        elif line and not line.startswith("#"):
            name = line.split("?", 1)[0].rstrip("/").split("/")[-1]
            line = prefix + name + suffix
        out.append(line)
    return "\n".join(out) + "\n"


def _hls_upstream(cam: dict, name: str) -> str:
    playlist = cam.get("hls") or ""
    if name == "enc.key":
        if "://" in playlist:
            origin = playlist.split("/", 3)[2]
            scheme = playlist.split(":", 1)[0]
            return f"{scheme}://{origin}/enc.key"
        return name
    if playlist:
        return playlist.rsplit("/", 1)[0] + "/" + name
    return name


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
        upstream = origin_get(cam["hls"])
        if upstream.status_code >= 400:
            raise HTTPException(status_code=502, detail=f"hls origin HTTP {upstream.status_code}")
        text = _rewrite_playlist(upstream.text, camera_id, token)
        return PlainTextResponse(text, media_type="application/vnd.apple.mpegurl")
    if not sess:
        raise HTTPException(status_code=503, detail="open a session first")
    raise HTTPException(status_code=503, detail="rtsp remux unavailable; install ffmpeg or use HLS")


@router.get("/api/stream/{camera_id}/hls/{name}")
def stream_hls_part(camera_id: str, name: str, token: str = Query(...)) -> Response:
    verify_stream_token(token, camera_id)
    if not _HLS_PART.match(name):
        raise HTTPException(status_code=400, detail="bad hls part")
    cam = store.get_camera(camera_id)
    if not cam:
        raise HTTPException(status_code=404, detail="unknown camera")
    url = _hls_upstream(cam, name)
    upstream = origin_get(url)
    if upstream.status_code >= 400:
        raise HTTPException(status_code=502, detail=f"hls part HTTP {upstream.status_code}")
    media = "application/octet-stream"
    if name.endswith(".ts"):
        media = "video/mp2t"
    elif name.endswith(".key"):
        media = "application/octet-stream"
    elif name.endswith(".m3u8"):
        media = "application/vnd.apple.mpegurl"
    return Response(content=upstream.content, media_type=media)
