from __future__ import annotations

from pathlib import Path

from app import config


def resolve_media_path(url: str) -> Path:
    path = Path(url)
    if not path.is_absolute():
        path = config.ROOT / url
    path = path.resolve()
    allowed = [
        (config.ROOT / "data").resolve(),
        config.SAMPLES_DIR.resolve(),
        (config.REPO_ROOT / "03_Data").resolve(),
    ]
    if not any(path == root or root in path.parents for root in allowed):
        raise ValueError("file url outside media roots")
    return path


def capture_url(camera: dict) -> tuple[str, str]:
    protocol = (camera.get("protocol") or "").lower()
    if protocol == "file":
        return str(resolve_media_path(camera.get("url") or "")), "file"
    if protocol == "hls" or (not camera.get("rtsp") and camera.get("hls")):
        return camera.get("hls") or camera.get("url") or "", "hls"
    return camera.get("rtsp") or camera.get("url") or "", "rtsp"
