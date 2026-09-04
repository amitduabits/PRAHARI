"""T-V07: original crop uri set; reconstructed face is pending_review, not auto CRITICAL."""

from __future__ import annotations

import numpy as np

from app.services import matcher
from app.services.crops import persist


def test_original_uri_and_allowed_methods(tmp_path, monkeypatch):
    monkeypatch.setenv("CROP_DIR", str(tmp_path / "crops"))
    crop = np.zeros((32, 32, 3), dtype=np.uint8)
    crop[:] = (40, 40, 40)
    meta = persist("CAM-OWN-001", "crop-1", crop, entity_type="vehicle")
    assert meta["crop_uri_original"]
    assert meta["crop_uri"] == meta["crop_uri_original"]
    assert meta["enhancement_method"] in {"none", "cubic_upscale", "blur_review"}


def test_reconstructed_does_not_auto_critical(client):
    matcher.reload()
    hit = matcher.on_detection(
        {
            "event_id": "recon-1",
            "entity_type": "person",
            "face_id": "WL-004",
            "entity_id": "WL-004",
            "plate": "",
            "camera_id": "CAM-OWN-001",
            "ts": "2026-08-31T12:05:00+05:30",
            "is_ai_reconstructed": 1,
        },
        notify=False,
    )
    assert hit is not None
    assert hit["status"] == "pending_review"
    assert hit["status"] != "open"
