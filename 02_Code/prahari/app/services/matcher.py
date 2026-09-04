"""O(1) watchlist match: plate, face_id/gallery_id, or intrusion. 120 s same-entity+camera dedupe."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from app import store

log = logging.getLogger("prahari.matcher")

DEDUPE_S = 120
_plates: dict[str, dict[str, Any]] = {}
_faces: dict[str, dict[str, Any]] = {}


def reload() -> None:
    global _plates, _faces
    items = store.list_watchlist()
    plates: dict[str, dict[str, Any]] = {}
    faces: dict[str, dict[str, Any]] = {}
    for item in items:
        plate = (item.get("plate") or "").strip().upper()
        if plate:
            plates[plate] = item
        gid = (item.get("gallery_id") or "").strip()
        if not gid and (item.get("entity_type") or "").lower() == "person":
            gid = (item.get("source_case_id") or "").strip()
        if gid:
            faces[gid] = item
            faces[item.get("source_case_id") or gid] = item
    _plates = plates
    _faces = faces


def match(plate: str | None) -> dict[str, Any] | None:
    if not plate:
        return None
    if not _plates and not _faces:
        reload()
    return _plates.get(plate.upper())


def match_face(face_id: str | None) -> dict[str, Any] | None:
    if not face_id:
        return None
    if not _plates and not _faces:
        reload()
    return _faces.get(face_id)


def _parse_ts(ts: str) -> datetime:
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        return datetime.now()


def _same_entity(existing: dict[str, Any], plate: str, face_id: str, entity_type: str, entity_id: str) -> bool:
    if plate and existing.get("plate") == plate:
        return True
    if face_id and (existing.get("entity_id") == face_id or existing.get("entity_id") == entity_id):
        return True
    if entity_type == "intrusion" and existing.get("entity_type") == "intrusion":
        return True
    return False


def on_detection(event: dict[str, Any], notify: bool = True) -> dict[str, Any] | None:
    if not _plates and not _faces:
        reload()
    entity_type = (event.get("entity_type") or "").lower()
    plate = (event.get("plate") or "").upper()
    face_id = (event.get("face_id") or "") or (
        event.get("entity_id") or "" if entity_type == "person" else ""
    )
    entity_id = event.get("entity_id") or plate or face_id or ""
    row: dict[str, Any] | None = None
    if entity_type == "intrusion":
        row = {
            "category": "INTRUSION",
            "priority": "CRITICAL",
            "source_case_id": "INTRUSION",
        }
    elif plate:
        row = _plates.get(plate)
    elif face_id:
        row = _faces.get(face_id)
    if not row:
        return None
    camera_id = event.get("camera_id") or ""
    ts = event.get("ts") or store.now_iso()
    t = _parse_ts(ts)
    open_alerts = [a for a in store.list_alerts(status="open") if a.get("camera_id") == camera_id]
    for existing in open_alerts:
        if not _same_entity(existing, plate, face_id, entity_type, entity_id):
            continue
        prev = _parse_ts(existing.get("ts") or ts)
        delta = abs((t - prev).total_seconds())
        if delta <= DEDUPE_S:
            counter = int(existing.get("counter") or 1) + 1
            store.update_alert_counter(existing["alert_id"], counter, event.get("event_id") or "")
            existing["counter"] = counter
            if notify and existing.get("priority") == "CRITICAL":
                from app.services import bus

                bus.notify(existing)
            return existing
    alert = store.insert_alert(
        {
            "event_id": event.get("event_id") or "",
            "plate": plate,
            "camera_id": camera_id,
            "ts": ts,
            "category": row.get("category") or event.get("category") or "",
            "priority": row.get("priority") or event.get("priority") or "LOW",
            "status": "open",
            "counter": 1,
            "entity_type": entity_type or ("person" if face_id else "vehicle"),
            "entity_id": entity_id,
        }
    )
    if notify:
        from app.services import bus

        bus.notify(alert)
    return alert


def seed_from_detections() -> int:
    reload()
    if store.fetchone("SELECT COUNT(*) AS n FROM alerts")["n"] > 0:
        return 0
    n = 0
    for det in store.list_detections():
        if on_detection(det, notify=False):
            n += 1
    return n
