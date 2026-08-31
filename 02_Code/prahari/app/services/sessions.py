"""Playback sessions. FFmpeg remux uses -rtsp_transport tcp. Consume only."""

from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path

from app import config
from app.paths import capture_url, resolve_media_path

log = logging.getLogger("prahari.sessions")

_SESSIONS: dict[str, dict] = {}


def active() -> list[str]:
    return list(_SESSIONS.keys())


def start(camera: dict) -> dict:
    cid = camera["camera_id"]
    if cid in _SESSIONS:
        return {"camera_id": cid, "status": "already_open"}
    if len(_SESSIONS) >= config.MAX_OPEN_CAPTURES:
        raise RuntimeError(
            f"MAX_OPEN_CAPTURES={config.MAX_OPEN_CAPTURES} reached. Close a tile first."
        )
    protocol = (camera.get("protocol") or "").lower()
    if protocol == "file":
        path = resolve_media_path(camera.get("url") or "")
        _SESSIONS[cid] = {"kind": "file", "path": str(path)}
        return {"camera_id": cid, "status": "open", "kind": "file"}
    if camera.get("hls"):
        _SESSIONS[cid] = {"kind": "hls", "url": camera["hls"]}
        return {"camera_id": cid, "status": "open", "kind": "hls"}
    url, proto = capture_url(camera)
    ffmpeg = shutil.which("ffmpeg")
    if proto == "rtsp" and ffmpeg and url:
        out_dir = config.ROOT / "data" / "hls" / cid
        out_dir.mkdir(parents=True, exist_ok=True)
        playlist = out_dir / "index.m3u8"
        cmd = [
            ffmpeg,
            "-rtsp_transport",
            "tcp",
            "-i",
            url,
            "-c",
            "copy",
            "-f",
            "hls",
            "-hls_time",
            "2",
            "-hls_list_size",
            "5",
            "-hls_flags",
            "delete_segments",
            str(playlist),
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        _SESSIONS[cid] = {"kind": "ffmpeg", "proc": proc, "dir": str(out_dir)}
        return {"camera_id": cid, "status": "open", "kind": "ffmpeg"}
    _SESSIONS[cid] = {"kind": "pending_rtsp", "url": url}
    return {"camera_id": cid, "status": "open", "kind": "pending_rtsp"}


def stop(camera_id: str) -> None:
    sess = _SESSIONS.pop(camera_id, None)
    if not sess:
        return
    proc = sess.get("proc")
    if proc is not None:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
    folder = sess.get("dir")
    if folder:
        for child in Path(folder).glob("*"):
            child.unlink(missing_ok=True)


def get(camera_id: str) -> dict | None:
    return _SESSIONS.get(camera_id)
