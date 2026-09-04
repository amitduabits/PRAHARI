from __future__ import annotations

import json

import numpy as np

from app.services.intrusion import check


def _cam(roi=None):
    if roi is None:
        roi = [[0, 0.5], [1, 0.5], [1, 1], [0, 1]]
    return {
        "camera_id": "CAM-FCS-001",
        "extra_json": json.dumps({"roi": roi}),
        "cam_type": "godown",
    }


def test_person_in_roi_is_critical():
    frame = np.zeros((360, 640, 3), dtype=np.uint8)
    obj = {
        "object_class": "person",
        "confidence": 0.7,
        "bbox": [100, 200, 80, 140],
        "crop_bgr": frame[200:340, 100:180],
    }
    hit = check(frame, _cam(), [obj])
    assert hit is not None
    assert hit["entity_type"] == "intrusion"
    assert hit["priority"] == "CRITICAL"


def test_person_outside_roi_no_event():
    frame = np.zeros((360, 640, 3), dtype=np.uint8)
    obj = {"object_class": "person", "confidence": 0.7, "bbox": [10, 10, 40, 40]}
    assert check(frame, _cam(), [obj]) is None


def test_missing_roi_no_crash():
    frame = np.zeros((360, 640, 3), dtype=np.uint8)
    obj = {"object_class": "person", "bbox": [100, 200, 80, 140]}
    assert check(frame, {"camera_id": "CAM-FCS-001", "extra_json": ""}, [obj]) is None


def test_intrusion_dedupes(client, auth):
    from app.services import matcher

    matcher.reload()
    first = matcher.on_detection(
        {
            "event_id": "intr-1",
            "entity_type": "intrusion",
            "entity_id": "CAM-FCS-001",
            "camera_id": "CAM-FCS-001",
            "ts": "2026-08-31T08:00:00+05:30",
        },
        notify=False,
    )
    assert first is not None
    assert first["priority"] == "CRITICAL"
    second = matcher.on_detection(
        {
            "event_id": "intr-2",
            "entity_type": "intrusion",
            "entity_id": "CAM-FCS-001",
            "camera_id": "CAM-FCS-001",
            "ts": "2026-08-31T08:00:10+05:30",
        },
        notify=False,
    )
    assert second["alert_id"] == first["alert_id"]
    assert second["counter"] == first["counter"] + 1
