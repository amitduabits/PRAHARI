from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_analyse_source_refuses_cam_prefix():
    text = (ROOT / "app" / "services" / "analyse.py").read_text(encoding="utf-8")
    assert "frs_refused" in text
    assert "cam\\d+" in text or r"^cam\d+" in text
    assert 'ownership") or "") != "Own"' in text or '!= "Own"' in text


def test_runtime_gov_camera_zero_person_events(client, auth):
    from io import BytesIO

    from PIL import Image

    buf = BytesIO()
    Image.new("RGB", (64, 64), (200, 160, 130)).save(buf, format="PNG")
    res = client.post(
        "/api/ingest/analyse",
        files={"file": ("skin.png", BytesIO(buf.getvalue()), "image/png")},
        data={"camera_id": "CAM-VAL-001", "engines": "anpr,objects,faces"},
        auth=auth,
    )
    assert res.status_code == 200
    people = [e for e in res.json()["events"] if e.get("entity_type") == "person"]
    assert people == []
