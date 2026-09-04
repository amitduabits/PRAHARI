"""Keyword filter over detections. Labelled keyword_rules, not a language model."""

from __future__ import annotations

import re
from typing import Any

from app import store
from app.services.plates import normalise

_PLATE_RE = re.compile(r"\b([A-Z]{2}\s?\d{1,2}\s?[A-Z]{1,3}\s?\d{3,4})\b", re.I)
_CAM_RE = re.compile(r"\b(CAM-[A-Z0-9-]+|cam\d+)\b", re.I)
_CLASSES = ("person", "car", "motorcycle", "bus", "truck", "bicycle", "intrusion")


def parse_rules(q: str) -> dict[str, str]:
    text = (q or "").strip()
    filters: dict[str, str] = {}
    plate_m = _PLATE_RE.search(text)
    if plate_m:
        plate = normalise(plate_m.group(1))
        if plate:
            filters["plate"] = plate
    cam_m = _CAM_RE.search(text)
    if cam_m:
        filters["camera_id"] = cam_m.group(1)
    lower = text.lower()
    for cls in _CLASSES:
        if re.search(rf"\b{re.escape(cls)}\b", lower):
            filters["object_class"] = cls
            break
    return filters


def run(q: str, limit: int = 50) -> dict[str, Any]:
    filters = parse_rules(q)
    plate = filters.get("plate")
    camera_id = filters.get("camera_id")
    rows = store.list_detections(plate=plate, camera_id=camera_id)
    cls = filters.get("object_class")
    if cls:
        rows = [
            r
            for r in rows
            if (r.get("object_class") or "").lower() == cls
            or (r.get("entity_type") or "").lower() == cls
        ]
    hits = rows[: max(1, min(int(limit or 50), 200))]
    return {
        "engine": "keyword_rules",
        "query": q,
        "filters": filters,
        "hits": hits,
        "count": len(hits),
    }
