"""Sentinel catalogue client. Camera ids change; JSON fields are the contract.

Live portal (2026-09-03): session cookie, GET /cameras.json as [{id, name}].
HLS at https://<web-host>/<id>/index.m3u8 (browser User-Agent required).
RTSP/WHEP on the public IP from the live /resource page, not on the TLS host.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import httpx

from app import config

FIXTURE_PATH = config.ROOT / "tests" / "fixtures" / "catalogue_sample.json"
CACHE_PATH = config.REPO_ROOT / "03_Data" / "sentinel_catalogue" / "catalogue.last.json"

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

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

_SESSION: dict[str, Any] = {"client": None, "base": ""}


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


def web_base(host: str) -> str:
    host = (host or "").strip()
    if not host:
        return ""
    if "://" in host:
        return host.rstrip("/")
    return "https://" + host.rstrip("/")


def apply_origin_urls(cam: dict[str, Any], web: str, rtsp_host: str = "") -> dict[str, Any]:
    """Fill HLS/RTSP/WHEP only when the catalogue row omitted them.

    Camera identity still comes from JSON. The live /resource page documents
    these origins; ids are never invented here.
    """
    cid = cam.get("id") or ""
    web = (web or "").rstrip("/")
    rtsp_host = (rtsp_host or "").strip()
    if cid and web and not cam.get("hls"):
        cam["hls"] = web + "/" + cid + "/index.m3u8"
    if cid and rtsp_host and not cam.get("rtsp"):
        cam["rtsp"] = "rtsp://" + rtsp_host + ":8554/stream/" + cid
    if cid and rtsp_host and not cam.get("whep"):
        cam["whep"] = "http://" + rtsp_host + ":8889/stream/" + cid + "/whep"
    return cam


def _looks_json(response: httpx.Response) -> bool:
    ctype = (response.headers.get("content-type") or "").lower()
    if "json" in ctype:
        return True
    text = response.text.lstrip()
    return text.startswith("{") or text.startswith("[")


def _login(client: httpx.Client, base: str) -> None:
    password = config.getenv("SENTINEL_PASSWORD", "").strip()
    if not password:
        return
    client.post(base + "/auth/login", data={"password": password})


def session(host: str | None = None) -> tuple[httpx.Client, str]:
    host = (host if host is not None else config.getenv("SENTINEL_HOST", "")).strip()
    base = web_base(host)
    if _SESSION["client"] is not None and _SESSION["base"] == base:
        return _SESSION["client"], base
    if _SESSION["client"] is not None:
        _SESSION["client"].close()
    client = httpx.Client(
        timeout=20.0,
        follow_redirects=True,
        headers={"User-Agent": BROWSER_UA, "Referer": base + "/", "Accept": "*/*"},
    )
    _login(client, base)
    _SESSION["client"] = client
    _SESSION["base"] = base
    return client, base


def origin_get(url: str, host: str | None = None) -> httpx.Response:
    client, _ = session(host)
    response = client.get(url)
    if response.status_code in {401, 403} or (
        response.status_code == 200 and "sign in" in response.text[:400].lower()
    ):
        _login(client, _SESSION["base"])
        response = client.get(url)
    return response


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
    client, base = session(host)
    configured = config.getenv("SENTINEL_CATALOGUE_PATH", "/cameras.json") or "/cameras.json"
    if not configured.startswith("/"):
        configured = "/" + configured
    candidates = [configured]
    for alt in ("/cameras.json", "/api/ingest"):
        if alt not in candidates:
            candidates.append(alt)
    last_error = "catalogue unreachable"
    payload: Any = None
    for path in candidates:
        response = client.get(base + path)
        if response.status_code == 404:
            last_error = f"{path} HTTP 404"
            continue
        if not _looks_json(response):
            if not config.getenv("SENTINEL_PASSWORD", "").strip():
                raise RuntimeError(
                    "catalogue is session-gated; set SENTINEL_PASSWORD in .env"
                )
            _login(client, base)
            response = client.get(base + path)
        if not _looks_json(response):
            last_error = f"{path} HTTP {response.status_code} not JSON"
            continue
        payload = response.json()
        break
    if payload is None:
        raise RuntimeError(last_error)
    save_cache(payload)
    cams = parse_payload(payload)
    rtsp_host = config.getenv("SENTINEL_RTSP_HOST", "").strip()
    return [apply_origin_urls(c, base, rtsp_host) for c in cams if c.get("id")]


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
