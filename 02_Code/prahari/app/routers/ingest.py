from __future__ import annotations

import uuid
from pathlib import Path

import cv2
import numpy as np
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from app import config, store
from app.auth import User, assert_write, require_user
from app.services import matcher
from app.services.anpr import recognize
from app.services.plates import normalise

router = APIRouter()


class ConfirmIn(BaseModel):
    camera_id: str
    plate: str
    ts: str | None = None


def _write_crop(camera_id: str, event_id: str, crop_bgr) -> str:
    folder = config.crop_dir() / camera_id
    folder.mkdir(parents=True, exist_ok=True)
    dest = folder / f"{event_id}.jpg"
    if crop_bgr is not None:
        cv2.imwrite(str(dest), crop_bgr)
    rel = f"/crops/{camera_id}/{event_id}.jpg"
    return rel, dest


def _camera_or_404(camera_id: str) -> dict:
    cam = store.get_camera(camera_id)
    if not cam:
        raise HTTPException(status_code=404, detail="unknown camera")
    return cam


def _event_from_anpr(cam: dict, result: dict, pts_ms: int = 0) -> dict:
    wl = matcher.match(result.get("plate"))
    event = {
        "event_id": str(uuid.uuid4()),
        "plate": result.get("plate") or "",
        "plate_raw": result.get("plate_raw") or "",
        "confidence": float(result.get("confidence") or 0),
        "camera_id": cam["camera_id"],
        "lat": cam.get("lat") or 0,
        "lon": cam.get("lon") or 0,
        "ts": store.now_iso(),
        "pts_ms": pts_ms,
        "crop_uri": "",
        "category": (wl or {}).get("category") or "",
        "priority": (wl or {}).get("priority") or "",
        "source_case_id": (wl or {}).get("source_case_id") or "",
    }
    rel, _ = _write_crop(cam["camera_id"], event["event_id"], result.get("crop_bgr"))
    event["crop_uri"] = rel
    return event


@router.post("/api/ingest/frame")
async def ingest_frame(
    file: UploadFile = File(...),
    camera_id: str = Form("CAM-OWN-001"),
    user: User = Depends(require_user),
) -> dict:
    assert_write(user)
    cam = _camera_or_404(camera_id)
    data = await file.read()
    arr = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if frame is None:
        raise HTTPException(status_code=400, detail="could not decode image")
    result = recognize(frame)
    if not result.get("plate"):
        return {"plate": None, "plate_raw": result.get("plate_raw"), "confidence": result.get("confidence"), "inserted": False}
    event = _event_from_anpr(cam, result)
    store.insert_detection(event)
    alert = matcher.on_detection(event)
    return {"inserted": True, "event": event, "alert": alert}


@router.post("/api/ingest/confirm")
def ingest_confirm(body: ConfirmIn, user: User = Depends(require_user)) -> dict:
    assert_write(user)
    plate = normalise(body.plate)
    if not plate:
        raise HTTPException(status_code=400, detail="plate failed Indian normaliser")
    cam = _camera_or_404(body.camera_id)
    wl = matcher.match(plate)
    event = {
        "event_id": str(uuid.uuid4()),
        "plate": plate,
        "plate_raw": body.plate,
        "confidence": 1.0,
        "camera_id": cam["camera_id"],
        "lat": cam.get("lat") or 0,
        "lon": cam.get("lon") or 0,
        "ts": body.ts or store.now_iso(),
        "pts_ms": 0,
        "crop_uri": "",
        "category": (wl or {}).get("category") or "",
        "priority": (wl or {}).get("priority") or "",
        "source_case_id": (wl or {}).get("source_case_id") or "",
    }
    store.insert_detection(event)
    store.audit(user.username, "operator_confirm", f"{plate}@{cam['camera_id']}")
    alert = matcher.on_detection(event)
    return {"inserted": True, "event": event, "alert": alert}


@router.get("/api/detections")
def detections(
    plate: str | None = None,
    camera_id: str | None = None,
    user: User = Depends(require_user),
) -> list[dict]:
    rows = store.list_detections(plate=plate, camera_id=camera_id)
    if user.role == "dept_viewer":
        allowed = {c["camera_id"] for c in store.list_cameras(department=user.department)}
        rows = [r for r in rows if r.get("camera_id") in allowed]
    return rows
