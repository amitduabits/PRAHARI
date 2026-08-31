from __future__ import annotations

import csv
import io
import math
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app import config, store
from app.auth import User, assert_write, can_see_camera, require_user, visible_cameras
from app.db import _as_float, _as_int
from app.present import camera_public
from app.services.catalogue import fetch, to_registry_row
from app.services import health_probe

router = APIRouter()


class CameraIn(BaseModel):
    camera_id: str
    department: str = ""
    ownership: str = "Gov"
    consent: bool = True
    lat: float
    lon: float
    protocol: str = "rtsp"
    url: str = ""
    retention_days: int = 7
    cam_type: str = ""
    health: str = "unknown"
    location: str = ""
    codec: str = ""
    width: int = 0
    height: int = 0
    rtsp: str = ""
    whep: str = ""
    hls: str = ""


def _validate(payload: dict[str, Any]) -> None:
    if not math.isfinite(float(payload.get("lat") or 0)) or not math.isfinite(float(payload.get("lon") or 0)):
        raise HTTPException(status_code=400, detail="lat/lon must be finite")
    ownership = payload.get("ownership") or "Gov"
    consent = payload.get("consent")
    if ownership == "Private-Permitted" and not consent:
        raise HTTPException(status_code=400, detail="Private-Permitted cameras require consent=true")


@router.get("/api/cameras")
def list_cameras(
    department: str | None = None,
    health: str | None = None,
    ownership: str | None = None,
    user: User = Depends(require_user),
) -> list[dict[str, Any]]:
    rows = store.list_cameras(department=department, health=health, ownership=ownership)
    return [camera_public(c, user) for c in visible_cameras(rows, user)]


@router.get("/api/cameras/{camera_id}")
def get_camera(camera_id: str, user: User = Depends(require_user)) -> dict[str, Any]:
    row = store.get_camera(camera_id)
    if not row:
        raise HTTPException(status_code=404, detail="unknown camera")
    if not can_see_camera(row, user):
        raise HTTPException(status_code=403, detail="forbidden")
    return camera_public(row, user)


@router.post("/api/cameras")
def create_camera(body: CameraIn, user: User = Depends(require_user)) -> dict[str, Any]:
    assert_write(user)
    payload = body.model_dump()
    _validate(payload)
    if store.get_camera(payload["camera_id"]):
        raise HTTPException(status_code=409, detail="camera_id exists")
    payload["consent"] = 1 if payload.get("consent") else 0
    store.upsert_camera(payload)
    store.audit(user.username, "camera_onboard", payload["camera_id"])
    row = store.get_camera(payload["camera_id"])
    return camera_public(row, user)


@router.post("/api/cameras/import")
async def import_csv(file: UploadFile = File(...), user: User = Depends(require_user)) -> dict:
    assert_write(user)
    raw = (await file.read()).decode("utf-8")
    reader = csv.DictReader(io.StringIO(raw))
    count = 0
    for row in reader:
        payload = {
            "camera_id": row["camera_id"],
            "department": row.get("department", ""),
            "ownership": row.get("ownership", "Gov"),
            "consent": _as_int(row.get("consent"), 0),
            "lat": _as_float(row.get("lat")),
            "lon": _as_float(row.get("lon")),
            "protocol": row.get("protocol", ""),
            "url": row.get("url", ""),
            "retention_days": _as_int(row.get("retention_days"), 0),
            "cam_type": row.get("cam_type", ""),
            "health": row.get("health", "unknown"),
            "location": row.get("location", ""),
            "codec": row.get("codec", ""),
            "width": _as_int(row.get("width")),
            "height": _as_int(row.get("height")),
            "rtsp": row.get("rtsp", ""),
            "whep": row.get("whep", ""),
            "hls": row.get("hls", ""),
            "extra_json": "",
        }
        _validate({**payload, "consent": bool(payload["consent"])})
        store.upsert_camera(payload)
        count += 1
    store.audit(user.username, "camera_import", f"n={count}")
    return {"imported": count}


@router.get("/api/cameras/export.csv")
def export_csv(user: User = Depends(require_user)) -> StreamingResponse:
    rows = visible_cameras(store.list_cameras(), user)
    buf = io.StringIO()
    fields = [
        "camera_id", "department", "ownership", "consent", "lat", "lon", "protocol",
        "retention_days", "cam_type", "health", "location", "codec", "width", "height",
    ]
    writer = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    store.audit(user.username, "camera_export", f"n={len(rows)}")
    buf.seek(0)
    return StreamingResponse(iter([buf.getvalue()]), media_type="text/csv")


@router.post("/api/cameras/sync-catalogue")
def sync_catalogue(user: User = Depends(require_user)) -> dict:
    assert_write(user)
    host = config.getenv("SENTINEL_HOST", "").strip()
    if not host:
        raise HTTPException(status_code=400, detail="SENTINEL_HOST not configured")
    cams = fetch(host)
    for cam in cams:
        store.upsert_camera(to_registry_row(cam))
    store.audit(user.username, "sync_catalogue", f"n={len(cams)}")
    return {"synced": len(cams), "live": sum(1 for c in cams if c.get("live"))}


@router.post("/api/cameras/probe")
def probe(user: User = Depends(require_user)) -> dict:
    assert_write(user)
    return health_probe.probe_reachable()


@router.get("/api/gap-report")
def gap_report(user: User = Depends(require_user)) -> dict:
    rows = visible_cameras(store.list_cameras(), user)
    offline = [c["camera_id"] for c in rows if c.get("health") == "offline"]
    short_retention = [
        {"camera_id": c["camera_id"], "retention_days": c.get("retention_days")}
        for c in rows
        if int(c.get("retention_days") or 0) < 8 and c.get("ownership") != "Own"
    ]
    missing_coords = [
        c["camera_id"]
        for c in rows
        if float(c.get("lat") or 0) == 0
        and float(c.get("lon") or 0) == 0
        and c.get("ownership") != "Own"
    ]
    private_without_consent = [
        c["camera_id"]
        for c in rows
        if c.get("ownership") == "Private-Permitted" and not c.get("consent")
    ]
    counts: dict[str, int] = {}
    for c in rows:
        dept = c.get("department") or "unknown"
        counts[dept] = counts.get(dept, 0) + 1
    return {
        "offline": offline,
        "short_retention": short_retention,
        "missing_coords": missing_coords,
        "private_without_consent": private_without_consent,
        "counts_by_department": counts,
        "sentinel_host_configured": config.sentinel_host_configured(),
        "total": len(rows),
    }
