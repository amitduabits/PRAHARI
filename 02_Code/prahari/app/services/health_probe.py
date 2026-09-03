"""Sequential health probes. Never open the whole grid at once."""

from __future__ import annotations

import json
import logging

from app import config, store
from app.paths import capture_url, resolve_media_path

log = logging.getLogger("prahari.probe")


def _fail_count(cam: dict) -> int:
    try:
        extra = json.loads(cam.get("extra_json") or "{}")
    except json.JSONDecodeError:
        extra = {}
    return int(extra.get("fail_count") or 0)


def _set_fail(camera_id: str, health: str, fail_count: int) -> None:
    cam = store.get_camera(camera_id) or {}
    try:
        extra = json.loads(cam.get("extra_json") or "{}")
    except json.JSONDecodeError:
        extra = {}
    extra["fail_count"] = fail_count
    store.set_camera_health(camera_id, health, extra)


def probe_one(cam: dict) -> str:
    protocol = (cam.get("protocol") or "").lower()
    if protocol == "file":
        try:
            path = resolve_media_path(cam.get("url") or "")
        except ValueError:
            return "fail"
        return "live" if path.is_file() else "offline"
    url, proto = capture_url(cam)
    if not url:
        return cam.get("health") or "unknown"
    from app.services.capture import StreamSession

    session = StreamSession()
    try:
        session.open(url, proto)
        ok, _, _ = session.read(reconnect=False)
        return "live" if ok else "degraded"
    except Exception as exc:
        log.warning("probe %s failed: %s", cam.get("camera_id"), exc)
        return "fail"
    finally:
        session.close()


def probe_reachable() -> dict:
    rows = [c for c in store.list_cameras() if c.get("health") != "offline"]
    cap = config.MAX_OPEN_CAPTURES
    examined = rows[:cap]
    results = []
    for cam in examined:
        cid = cam["camera_id"]
        outcome = probe_one(cam)
        if outcome == "fail":
            fails = _fail_count(cam) + 1
            health = "offline" if fails >= 3 else (cam.get("health") or "unknown")
            _set_fail(cid, health, fails)
            store.audit("system", "health_probe", f"{cid} fail={fails} health={health}")
            results.append({"camera_id": cid, "health": health, "fails": fails})
        elif outcome in {"live", "degraded", "offline"}:
            _set_fail(cid, outcome, 0)
            results.append({"camera_id": cid, "health": outcome, "fails": 0})
        else:
            results.append({"camera_id": cid, "health": cam.get("health"), "skipped": True})
    return {"probed": results, "skipped_offline": True}
