from __future__ import annotations

import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app import store
from app.auth import User, require_user

router = APIRouter()
SPEED_CAP_KMH = 180


def _parse(ts: str) -> datetime | None:
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        return None


def build_track(plate: str) -> dict:
    plate = plate.upper()
    detections = store.list_detections(plate=plate)
    points = []
    category = ""
    for det in detections:
        cam = store.get_camera(det["camera_id"]) or {}
        category = det.get("category") or category
        points.append(
            {
                "ts": det.get("ts"),
                "camera_id": det.get("camera_id"),
                "location": cam.get("location") or "",
                "lat": det.get("lat") if det.get("lat") else cam.get("lat"),
                "lon": det.get("lon") if det.get("lon") else cam.get("lon"),
                "pts_ms": det.get("pts_ms"),
                "crop_uri": det.get("crop_uri"),
                "event_id": det.get("event_id"),
                "priority": det.get("priority"),
            }
        )
    flags = []
    for i in range(1, len(points)):
        a, b = points[i - 1], points[i]
        t0, t1 = _parse(a["ts"] or ""), _parse(b["ts"] or "")
        if not t0 or not t1:
            continue
        hours = abs((t1 - t0).total_seconds()) / 3600.0
        if hours <= 0:
            continue
        dist = store.haversine_km(float(a["lat"] or 0), float(a["lon"] or 0), float(b["lat"] or 0), float(b["lon"] or 0))
        speed = dist / hours
        if speed > SPEED_CAP_KMH:
            flags.append(
                {
                    "type": "teleport",
                    "from": a["camera_id"],
                    "to": b["camera_id"],
                    "note": f"implied {speed:.0f} km/h exceeds {SPEED_CAP_KMH}",
                }
            )
    return {"plate": plate, "category": category, "count": len(points), "points": points, "flags": flags}


@router.get("/api/track/{plate}")
def track(plate: str, user: User = Depends(require_user)) -> dict:
    return build_track(plate)


@router.get("/api/track/{plate}/report.csv")
def report_csv(plate: str, user: User = Depends(require_user)) -> StreamingResponse:
    data = build_track(plate)
    if data["count"] == 0:
        raise HTTPException(status_code=404, detail="no detections")
    buf = io.StringIO()
    fields = ["plate", "camera_id", "location", "lat", "lon", "ts", "pts_ms", "priority", "event_id"]
    writer = csv.DictWriter(buf, fieldnames=fields)
    writer.writeheader()
    for p in data["points"]:
        writer.writerow(
            {
                "plate": data["plate"],
                "camera_id": p["camera_id"],
                "location": p["location"],
                "lat": p["lat"],
                "lon": p["lon"],
                "ts": p["ts"],
                "pts_ms": p["pts_ms"],
                "priority": p.get("priority") or "",
                "event_id": p["event_id"],
            }
        )
    store.audit(user.username, "report_download", plate.upper())
    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=track_{plate.upper()}.csv"},
    )
