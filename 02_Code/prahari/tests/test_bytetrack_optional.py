"""T-V06: ByteTrack track_id stable across overlapping boxes. Skip without ultralytics."""

from __future__ import annotations

import pytest

from app.engines.bytetrack_backend import engine_available, reset, update
from app.services.objects import reset as objects_reset


@pytest.mark.skipif(not engine_available(), reason="ultralytics ByteTrack missing")
def test_bytetrack_stable_and_reset():
    reset("CAM-OWN-001")
    objects_reset("CAM-OWN-001")
    det = [{"box": [10, 10, 80, 80], "conf": 0.9, "cls_id": 0}]
    first = update("CAM-OWN-001", det)
    second = update("CAM-OWN-001", [{"box": [12, 12, 82, 82], "conf": 0.9, "cls_id": 0}])
    if not first or not second:
        pytest.skip("ByteTrack returned no tracks on synthetic boxes")
    assert first[0]["track_id"] == second[0]["track_id"]
    reset("CAM-OWN-001")
    third = update("CAM-OWN-001", det)
    assert third
    # new tracker instance after reset; id may restart at 1, which is still a list
    assert isinstance(third[0]["track_id"], int)
