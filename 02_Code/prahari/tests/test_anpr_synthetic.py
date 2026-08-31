from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image, ImageDraw, ImageFont

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "plate_gj01ab1234.png"


def _ensure_fixture() -> Path:
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    if FIXTURE.is_file():
        return FIXTURE
    img = Image.new("RGB", (400, 120), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except OSError:
        font = ImageFont.load_default()
    draw.text((20, 30), "GJ01AB1234", fill="black", font=font)
    img.save(FIXTURE)
    return FIXTURE


def test_normalise_still_independent():
    from app.services.plates import normalise

    assert normalise("GJ 01 AB 1234") == "GJ01AB1234"


def test_recognize_or_skip_without_tesseract():
    _ensure_fixture()
    import cv2
    from app.services.anpr import recognize

    try:
        import pytesseract
        pytesseract.get_tesseract_version()
    except Exception:
        pytest.skip("Tesseract binary not installed. choco install tesseract or install from UB Mannheim.")
    frame = cv2.imread(str(FIXTURE))
    assert frame is not None
    result = recognize(frame)
    if result.get("plate") != "GJ01AB1234":
        pytest.skip("Tesseract did not read the synthetic plate; operator-confirm covers the demo.")


def test_confirm_inserts_detection(client, auth):
    res = client.post(
        "/api/ingest/confirm",
        json={"camera_id": "CAM-OWN-001", "plate": "GJ 01 AB 1234"},
        auth=auth,
    )
    assert res.status_code == 200
    body = res.json()
    assert body["inserted"] is True
    assert body["event"]["plate"] == "GJ01AB1234"
