"""Sentinel /api/ingest client. Camera ids change; JSON fields are the contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx

from app import config

FIXTURE_PATH = config.ROOT / "tests" / "fixtures" / "catalogue_sample.json"
CACHE_PATH = config.REPO_ROOT / "03_Data" / "sentinel_catalogue" / "catalogue.last.json"

_ALIASES = {
    "id": ("id", "camera_id", "cameraid", "camid"),
    "location": ("location", "name", "site", "place"),
    "codec": ("codec", "video_codec", "encoding"),
    "live": ("live", "is_live", "online", "status"),
    "width": ("width", "w"),
    "height": ("height", "h"),
    "fps_declared": ("fps_declared", "fps", "frame_rate", "framerate"),
    "rtsp": ("rtsp", "rtsp_url", "rtspurl"),
    "whep": ("whep", "whep_url", "whepurl"),
    "hls": ("hls", "hlsurl", "hls_url", "m3u8"),
}


def _fold(raw: dict[str, Any]) -> dict[str, Any]:
    return {str(k).lower().replace("-", "_"): v for k, v in raw.items()}


def _pick(folded: dict[str, Any], field: str) -> Any:
    for alias in _ALIASES[field]:
        if alias in folded:
            return folded[alias]
    return None


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "live", "online", "yes"}


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def normalise_camera(raw: dict[str, Any]) -> dict[str, Any]:
    folded = _fold(raw)
    live_val = _pick(folded, "live")
    if isinstance(live_val, str) and live_val.lower() in {"offline", "down"}:
        live = False
    else:
        live = _as_bool(live_val) if live_val is not None else True
    cam_id = _pick(folded, "id")
    return {
        "id": str(cam_id) if cam_id is not None else "",
        "location": str(_pick(folded, "location") or ""),
        "codec": str(_pick(folded, "codec") or "").lower(),
        "live": live,
        "width": _as_int(_pick(folded, "width")),
        "height": _as_int(_pick(folded, "height")),
        "fps_declared": _as_float(_pick(folded, "fps_declared")),
        "rtsp": str(_pick(folded, "rtsp") or ""),
        "whep": str(_pick(folded, "whep") or ""),
        "hls": str(_pick(folded, "hls") or ""),
        "raw": raw,
    }


def parse_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        cameras = payload.get("cameras") or payload.get("Cameras") or payload.get("data") or []
    elif isinstance(payload, list):
        cameras = payload
    else:
        cameras = []
    return [normalise_camera(c) for c in cameras if isinstance(c, dict)]


def load_fixture(path: Path | None = None) -> list[dict[str, Any]]:
    target = path or FIXTURE_PATH
    payload = json.loads(target.read_text(encoding="utf-8"))
    return parse_payload(payload)


def save_cache(payload: Any) -> Path:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not isinstance(payload, (dict, list)):
        payload = {"cameras": payload}
    CACHE_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return CACHE_PATH


def fetch(host: str | None = None) -> list[dict[str, Any]]:
    host = (host if host is not None else config.getenv("SENTINEL_HOST", "")).strip()
    if not host:
        return load_fixture()
    base = host if "://" in host else f"http://{host}"
    url = base.rstrip("/") + config.getenv("SENTINEL_CATALOGUE_PATH", "/api/ingest")
    with httpx.Client(timeout=10.0, follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
        payload = response.json()
    save_cache(payload)
    return parse_payload(payload)


def to_registry_row(cam: dict[str, Any]) -> dict[str, Any]:
    protocol = "rtsp"
    url = cam.get("rtsp") or ""
    if not url and cam.get("hls"):
        protocol = "hls"
        url = cam["hls"]
    health = "live" if cam.get("live") else "offline"
    return {
        "camera_id": cam["id"],
        "department": "Sentinel",
        "ownership": "Gov",
        "consent": 1,
        "lat": 0.0,
        "lon": 0.0,
        "protocol": protocol,
        "url": url,
        "retention_days": 0,
        "cam_type": "sandbox",
        "health": health,
        "location": cam.get("location") or "",
        "codec": cam.get("codec") or "",
        "width": cam.get("width") or 0,
        "height": cam.get("height") or 0,
        "rtsp": cam.get("rtsp") or "",
        "whep": cam.get("whep") or "",
        "hls": cam.get("hls") or "",
        "extra_json": json.dumps({"fps_declared": cam.get("fps_declared"), "source": "catalogue"}),
    }
