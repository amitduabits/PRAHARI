"""O(1) watchlist match with 120 s same plate+camera dedupe."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from app import store

log = logging.getLogger("prahari.matcher")

DEDUPE_S = 120
_plates: set[str] = set()
_rows: dict[str, dict[str, Any]] = {}


def reload() -> None:
    global _plates, _rows
    items = store.list_watchlist()
    rows: dict[str, dict[str, Any]] = {}
    plates: set[str] = set()
    for item in items:
        plate = (item.get("plate") or "").strip().upper()
        if not plate:
            continue
        plates.add(plate)
        rows[plate] = item
    _plates = plates
    _rows = rows


def match(plate: str | None) -> dict[str, Any] | None:
    if not plate:
        return None
    if not _rows:
        reload()
    return _rows.get(plate.upper())


def _parse_ts(ts: str) -> datetime:
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        return datetime.now()


def on_detection(event: dict[str, Any], notify: bool = True) -> dict[str, Any] | None:
    if not _rows:
        reload()
    plate = (event.get("plate") or "").upper()
    row = match(plate)
    if not row:
        return None
    camera_id = event.get("camera_id") or ""
    ts = event.get("ts") or store.now_iso()
    t = _parse_ts(ts)
    open_alerts = [
        a
        for a in store.list_alerts(status="open")
        if a.get("plate") == plate and a.get("camera_id") == camera_id
    ]
    for existing in open_alerts:
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
            "category": row.get("category") or "",
            "priority": row.get("priority") or "LOW",
            "status": "open",
            "counter": 1,
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
