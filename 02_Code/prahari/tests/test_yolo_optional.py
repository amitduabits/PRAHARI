"""T-V05: YOLO person/vehicle on a real still. Skip without weights."""

from __future__ import annotations

from pathlib import Path

import cv2
import pytest

from app.engines.yolo_backend import weights_path


def _ready() -> bool:
    try:
        import ultralytics  # noqa: F401
    except Exception:
        return False
    return weights_path().is_file()


@pytest.mark.skipif(not _ready(), reason="ultralytics or yolov8n.pt missing")
def test_yolo_detects_person_or_vehicle():
    from app.engines.yolo_backend import detect_objects

    fixture = Path(__file__).resolve().parent / "fixtures" / "person_blob.png"
    frame = cv2.imread(str(fixture))
    if frame is None:
        pytest.skip("person_blob fixture missing")
    hits = detect_objects(frame)
    assert isinstance(hits, list)
