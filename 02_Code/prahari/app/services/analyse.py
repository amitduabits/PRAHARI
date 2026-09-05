"""Single analyse() entry. Faces are dropped for Gov cameras and camNN sandbox ids."""

from __future__ import annotations

import logging
import uuid
from typing import Any

import numpy as np

from app import config
from app.services import matcher
from app.services.anpr import recognize
from app.services.provenance import CAM_RE, faces_allowed

log = logging.getLogger("prahari.analyse")

_CAM_RE = CAM_RE


def engines_for(camera: dict) -> list[str]:
    raw = config.getenv("ANALYTICS_ENGINES", "anpr,objects")
    engines = [e.strip().lower() for e in raw.split(",") if e.strip()]
    cam_id = str(camera.get("camera_id") or "")
    ownership = str(camera.get("ownership") or "")
    if not faces_allowed(camera):
        engines = [e for e in engines if e != "faces"]
        log.info("frs_refused camera_id=%s ownership=%s", cam_id, ownership)
    return engines


def _base_event(camera: dict, pts_ms: int, **fields: Any) -> dict[str, Any]:
    event = {
        "event_id": str(uuid.uuid4()),
        "entity_type": fields.get("entity_type") or "vehicle",
        "entity_id": fields.get("entity_id") or "",
        "plate": fields.get("plate") or "",
        "plate_raw": fields.get("plate_raw") or "",
        "face_id": fields.get("face_id") or "",
        "object_class": fields.get("object_class") or "",
        "bbox": fields.get("bbox") or [0, 0, 0, 0],
        "track_id": fields.get("track_id") or "",
        "confidence": float(fields.get("confidence") or 0),
        "camera_id": camera.get("camera_id") or "",
        "lat": camera.get("lat") or 0,
        "lon": camera.get("lon") or 0,
        "ts": fields.get("ts") or "",
        "pts_ms": pts_ms,
        "crop_uri": "",
        "crop_bgr": fields.get("crop_bgr"),
        "category": fields.get("category") or "",
        "priority": fields.get("priority") or "",
        "source_case_id": fields.get("source_case_id") or "",
        "source": fields.get("source") or "",
    }
    wl = None
    if event["plate"]:
        wl = matcher.match(event["plate"])
    elif event["face_id"]:
        matcher.reload()
        wl = matcher.match_face(event["face_id"])
    if wl:
        event["category"] = event["category"] or wl.get("category") or ""
        event["priority"] = event["priority"] or wl.get("priority") or ""
        event["source_case_id"] = event["source_case_id"] or wl.get("source_case_id") or ""
    return event


def analyse(frame_bgr: np.ndarray, camera: dict, pts_ms: int = 0) -> list[dict]:
    """Run enabled engines. Return zero or more detection events (not yet inserted)."""
    events: list[dict] = []
    engines = engines_for(camera)
    cam_id = camera.get("camera_id") or ""

    if "anpr" in engines:
        try:
            result = recognize(frame_bgr)
        except Exception as exc:
            log.warning("anpr skipped: %s", exc)
            result = {}
        if result.get("plate"):
            events.append(
                _base_event(
                    camera,
                    pts_ms,
                    entity_type="vehicle",
                    entity_id=result.get("plate"),
                    plate=result.get("plate"),
                    plate_raw=result.get("plate_raw"),
                    confidence=result.get("confidence"),
                    bbox=result.get("box") or [0, 0, 0, 0],
                    crop_bgr=result.get("crop_bgr"),
                    source="anpr",
                )
            )

    object_hits: list[dict] = []
    if "objects" in engines:
        try:
            from app.services import objects as objects_mod

            object_hits = objects_mod.detect(frame_bgr, camera_id=cam_id)
        except Exception as exc:
            log.warning("objects skipped: %s", exc)
            object_hits = []
        for hit in object_hits:
            events.append(
                _base_event(
                    camera,
                    pts_ms,
                    entity_type="object",
                    entity_id=hit.get("object_class"),
                    object_class=hit.get("object_class"),
                    confidence=hit.get("confidence"),
                    bbox=hit.get("bbox"),
                    track_id=hit.get("track_id"),
                    crop_bgr=hit.get("crop_bgr"),
                    source="objects",
                )
            )

    if "faces" in engines:
        try:
            from app.services import faces as faces_mod

            for hit in faces_mod.match(frame_bgr):
                events.append(
                    _base_event(
                        camera,
                        pts_ms,
                        entity_type="person",
                        entity_id=hit.get("face_id") or "",
                        face_id=hit.get("face_id") or "",
                        confidence=hit.get("confidence"),
                        bbox=hit.get("bbox"),
                        crop_bgr=hit.get("crop_bgr"),
                        source="faces",
                    )
                )
        except Exception as exc:
            log.warning("faces skipped: %s", exc)

    if cam_id == "CAM-FCS-001" or (camera.get("cam_type") or "") == "godown":
        try:
            from app.services import intrusion as intrusion_mod

            hit = intrusion_mod.check(frame_bgr, camera, object_hits)
            if hit:
                events.append(_base_event(camera, pts_ms, **hit))
        except Exception as exc:
            log.warning("intrusion skipped: %s", exc)

    return events
