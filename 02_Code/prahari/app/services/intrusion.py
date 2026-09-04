"""Person-in-ROI intrusion. Wrapper on object detections, not a fourth network."""

from __future__ import annotations

import json
from typing import Any

import numpy as np


def roi_of(camera: dict) -> list[list[float]] | None:
    raw = camera.get("extra_json") or ""
    if not raw:
        return None
    if isinstance(raw, dict):
        data = raw
    else:
        try:
            data = json.loads(raw)
        except (TypeError, json.JSONDecodeError):
            return None
    roi = data.get("roi") if isinstance(data, dict) else None
    if not roi:
        return None
    return roi


def _person_area_in_roi(bbox: list[int], roi: list, frame_shape: tuple[int, ...]) -> float:
    h, w = frame_shape[:2]
    x, y, bw, bh = [int(v) for v in bbox]
    person = (x, y, x + bw, y + bh)
    if len(roi) == 4 and all(isinstance(v, (int, float)) for v in roi):
        x0, y0, x1, y1 = roi
        if 0 <= x0 <= 1 and 0 <= y0 <= 1:
            rx0, ry0, rx1, ry1 = int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)
        else:
            rx0, ry0, rx1, ry1 = int(x0), int(y0), int(x1), int(y1)
    else:
        xs = [p[0] for p in roi]
        ys = [p[1] for p in roi]
        if max(xs) <= 1.0 and max(ys) <= 1.0:
            rx0, rx1 = int(min(xs) * w), int(max(xs) * w)
            ry0, ry1 = int(min(ys) * h), int(max(ys) * h)
        else:
            rx0, rx1 = int(min(xs)), int(max(xs))
            ry0, ry1 = int(min(ys)), int(max(ys))
    ix0, iy0 = max(person[0], rx0), max(person[1], ry0)
    ix1, iy1 = min(person[2], rx1), min(person[3], ry1)
    inter = max(0, ix1 - ix0) * max(0, iy1 - iy0)
    area = max(1, bw * bh)
    return inter / area


def check(frame_bgr: np.ndarray, camera: dict, object_events: list[dict[str, Any]]) -> dict[str, Any] | None:
    roi = roi_of(camera)
    if roi is None or frame_bgr is None:
        return None
    for obj in object_events:
        if (obj.get("object_class") or "") != "person":
            continue
        bbox = obj.get("bbox") or [0, 0, 0, 0]
        overlap = _person_area_in_roi(bbox, roi, frame_bgr.shape)
        if overlap >= 0.30:
            return {
                "entity_type": "intrusion",
                "entity_id": camera.get("camera_id") or "",
                "object_class": "person",
                "category": "INTRUSION",
                "priority": "CRITICAL",
                "confidence": float(obj.get("confidence") or 0.5),
                "bbox": bbox,
                "crop_bgr": obj.get("crop_bgr"),
                "source": "intrusion",
            }
    return None
