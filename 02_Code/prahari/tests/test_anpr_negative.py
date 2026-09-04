from __future__ import annotations

from io import BytesIO

from PIL import Image


def test_blank_still_not_inserted(client, auth):
    buf = BytesIO()
    Image.new("RGB", (200, 80), "white").save(buf, format="PNG")
    res = client.post(
        "/api/ingest/frame",
        files={"file": ("blank.png", BytesIO(buf.getvalue()), "image/png")},
        data={"camera_id": "CAM-OWN-001"},
        auth=auth,
    )
    assert res.status_code == 200
    assert res.json()["inserted"] is False


def test_unknown_camera_404(client, auth):
    buf = BytesIO()
    Image.new("RGB", (20, 20), "white").save(buf, format="PNG")
    res = client.post(
        "/api/ingest/frame",
        files={"file": ("x.png", BytesIO(buf.getvalue()), "image/png")},
        data={"camera_id": "NO-SUCH-CAM"},
        auth=auth,
    )
    assert res.status_code == 404


def test_undecodable_bytes_400(client, auth):
    res = client.post(
        "/api/ingest/frame",
        files={"file": ("x.bin", BytesIO(b"not-an-image"), "application/octet-stream")},
        data={"camera_id": "CAM-OWN-001"},
        auth=auth,
    )
    assert res.status_code == 400
