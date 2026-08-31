"""SQLite helpers used by routers and services."""

from __future__ import annotations

import json
import math
import uuid
from datetime import datetime, timezone
from typing import Any

from app.db import connect
from app.models import row_to_dict


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def fetchall(sql: str, params: tuple | dict = ()) -> list[dict[str, Any]]:
    conn = connect()
    try:
        return [row_to_dict(r) for r in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()


def fetchone(sql: str, params: tuple | dict = ()) -> dict[str, Any] | None:
    conn = connect()
    try:
        row = conn.execute(sql, params).fetchone()
        return row_to_dict(row) if row else None
    finally:
        conn.close()


def execute(sql: str, params: tuple | dict = ()) -> None:
    conn = connect()
    try:
        conn.execute(sql, params)
        conn.commit()
    finally:
        conn.close()


def audit(actor: str, action: str, detail: str) -> None:
    execute(
        "INSERT INTO audit (ts, actor, action, detail) VALUES (?, ?, ?, ?)",
        (now_iso(), actor, action, detail[:800]),
    )


def list_cameras(
    department: str | None = None,
    health: str | None = None,
    ownership: str | None = None,
) -> list[dict[str, Any]]:
    sql = "SELECT * FROM cameras WHERE 1=1"
    params: list[Any] = []
    if department:
        sql += " AND department = ?"
        params.append(department)
    if health:
        sql += " AND health = ?"
        params.append(health)
    if ownership:
        sql += " AND ownership = ?"
        params.append(ownership)
    sql += " ORDER BY camera_id"
    return fetchall(sql, tuple(params))


def get_camera(camera_id: str) -> dict[str, Any] | None:
    return fetchone("SELECT * FROM cameras WHERE camera_id = ?", (camera_id,))


def upsert_camera(row: dict[str, Any]) -> None:
    execute(
        """
        INSERT INTO cameras (
            camera_id, department, ownership, consent, lat, lon, protocol, url,
            retention_days, cam_type, health, location, codec, width, height,
            rtsp, whep, hls, extra_json
        ) VALUES (
            :camera_id, :department, :ownership, :consent, :lat, :lon, :protocol, :url,
            :retention_days, :cam_type, :health, :location, :codec, :width, :height,
            :rtsp, :whep, :hls, :extra_json
        )
        ON CONFLICT(camera_id) DO UPDATE SET
            department=excluded.department,
            ownership=excluded.ownership,
            consent=excluded.consent,
            lat=excluded.lat,
            lon=excluded.lon,
            protocol=excluded.protocol,
            url=excluded.url,
            retention_days=excluded.retention_days,
            cam_type=excluded.cam_type,
            health=excluded.health,
            location=excluded.location,
            codec=excluded.codec,
            width=excluded.width,
            height=excluded.height,
            rtsp=excluded.rtsp,
            whep=excluded.whep,
            hls=excluded.hls,
            extra_json=excluded.extra_json
        """,
        {
            "camera_id": row["camera_id"],
            "department": row.get("department") or "",
            "ownership": row.get("ownership") or "Gov",
            "consent": int(row.get("consent") or 0),
            "lat": float(row.get("lat") or 0),
            "lon": float(row.get("lon") or 0),
            "protocol": row.get("protocol") or "",
            "url": row.get("url") or "",
            "retention_days": int(row.get("retention_days") or 0),
            "cam_type": row.get("cam_type") or "",
            "health": row.get("health") or "unknown",
            "location": row.get("location") or "",
            "codec": row.get("codec") or "",
            "width": int(row.get("width") or 0),
            "height": int(row.get("height") or 0),
            "rtsp": row.get("rtsp") or "",
            "whep": row.get("whep") or "",
            "hls": row.get("hls") or "",
            "extra_json": row.get("extra_json") or "",
        },
    )


def set_camera_health(camera_id: str, health: str, extra: dict | None = None) -> None:
    extra_json = json.dumps(extra) if extra is not None else None
    if extra_json is None:
        execute("UPDATE cameras SET health = ? WHERE camera_id = ?", (health, camera_id))
    else:
        execute(
            "UPDATE cameras SET health = ?, extra_json = ? WHERE camera_id = ?",
            (health, extra_json, camera_id),
        )


def insert_detection(event: dict[str, Any]) -> dict[str, Any]:
    if not event.get("event_id"):
        event = {**event, "event_id": str(uuid.uuid4())}
    execute(
        """
        INSERT INTO detections (
            event_id, plate, plate_raw, confidence, camera_id, lat, lon, ts,
            pts_ms, crop_uri, category, priority, source_case_id
        ) VALUES (
            :event_id, :plate, :plate_raw, :confidence, :camera_id, :lat, :lon, :ts,
            :pts_ms, :crop_uri, :category, :priority, :source_case_id
        )
        """,
        {
            "event_id": event["event_id"],
            "plate": event.get("plate") or "",
            "plate_raw": event.get("plate_raw") or "",
            "confidence": float(event.get("confidence") or 0),
            "camera_id": event.get("camera_id") or "",
            "lat": float(event.get("lat") or 0),
            "lon": float(event.get("lon") or 0),
            "ts": event.get("ts") or now_iso(),
            "pts_ms": int(event.get("pts_ms") or 0),
            "crop_uri": event.get("crop_uri") or "",
            "category": event.get("category") or "",
            "priority": event.get("priority") or "",
            "source_case_id": event.get("source_case_id") or "",
        },
    )
    return event


def list_detections(plate: str | None = None, camera_id: str | None = None) -> list[dict[str, Any]]:
    sql = "SELECT * FROM detections WHERE 1=1"
    params: list[Any] = []
    if plate:
        sql += " AND plate = ?"
        params.append(plate)
    if camera_id:
        sql += " AND camera_id = ?"
        params.append(camera_id)
    sql += " ORDER BY ts"
    return fetchall(sql, tuple(params))


def list_watchlist() -> list[dict[str, Any]]:
    return fetchall("SELECT * FROM watchlist ORDER BY source_case_id")


def get_watchlist_item(source_case_id: str) -> dict[str, Any] | None:
    return fetchone("SELECT * FROM watchlist WHERE source_case_id = ?", (source_case_id,))


def upsert_watchlist(row: dict[str, Any]) -> None:
    execute(
        """
        INSERT INTO watchlist (source_case_id, entity_type, plate, name, category, priority, source, notes)
        VALUES (:source_case_id, :entity_type, :plate, :name, :category, :priority, :source, :notes)
        ON CONFLICT(source_case_id) DO UPDATE SET
            entity_type=excluded.entity_type,
            plate=excluded.plate,
            name=excluded.name,
            category=excluded.category,
            priority=excluded.priority,
            source=excluded.source,
            notes=excluded.notes
        """,
        {
            "source_case_id": row["source_case_id"],
            "entity_type": row.get("entity_type") or "vehicle",
            "plate": row.get("plate") or "",
            "name": row.get("name") or "",
            "category": row.get("category") or "",
            "priority": row.get("priority") or "LOW",
            "source": row.get("source") or "",
            "notes": row.get("notes") or "",
        },
    )


def delete_watchlist(source_case_id: str) -> None:
    execute("DELETE FROM watchlist WHERE source_case_id = ?", (source_case_id,))


def list_alerts(status: str | None = None) -> list[dict[str, Any]]:
    if status:
        return fetchall(
            "SELECT * FROM alerts WHERE status = ? ORDER BY ts DESC", (status,)
        )
    return fetchall("SELECT * FROM alerts ORDER BY ts DESC")


def get_alert(alert_id: str) -> dict[str, Any] | None:
    return fetchone("SELECT * FROM alerts WHERE alert_id = ?", (alert_id,))


def insert_alert(row: dict[str, Any]) -> dict[str, Any]:
    if not row.get("alert_id"):
        row = {**row, "alert_id": str(uuid.uuid4())}
    execute(
        """
        INSERT INTO alerts (
            alert_id, event_id, plate, camera_id, ts, category, priority, status,
            ack_by, ack_ts, counter
        ) VALUES (
            :alert_id, :event_id, :plate, :camera_id, :ts, :category, :priority, :status,
            :ack_by, :ack_ts, :counter
        )
        """,
        {
            "alert_id": row["alert_id"],
            "event_id": row.get("event_id") or "",
            "plate": row.get("plate") or "",
            "camera_id": row.get("camera_id") or "",
            "ts": row.get("ts") or now_iso(),
            "category": row.get("category") or "",
            "priority": row.get("priority") or "LOW",
            "status": row.get("status") or "open",
            "ack_by": row.get("ack_by"),
            "ack_ts": row.get("ack_ts"),
            "counter": int(row.get("counter") or 1),
        },
    )
    return row


def update_alert_counter(alert_id: str, counter: int, event_id: str) -> None:
    execute(
        "UPDATE alerts SET counter = ?, event_id = ? WHERE alert_id = ?",
        (counter, event_id, alert_id),
    )


def ack_alert(alert_id: str, actor: str) -> None:
    execute(
        "UPDATE alerts SET status = ?, ack_by = ?, ack_ts = ? WHERE alert_id = ?",
        ("acked", actor, now_iso(), alert_id),
    )


def list_audit(limit: int = 200) -> list[dict[str, Any]]:
    return fetchall("SELECT * FROM audit ORDER BY id DESC LIMIT ?", (limit,))


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(min(1.0, math.sqrt(a)))
