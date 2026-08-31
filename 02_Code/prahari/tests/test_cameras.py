from pathlib import Path

SAMPLES = Path(__file__).resolve().parents[3] / "03_Data" / "samples" / "cameras.csv"


def test_import_and_gap_report(client, auth):
    text = SAMPLES.read_text(encoding="utf-8")
    files = {"file": ("cameras.csv", text, "text/csv")}
    res = client.post("/api/cameras/import", files=files, auth=auth)
    assert res.status_code == 200
    gap = client.get("/api/gap-report", auth=auth).json()
    assert "CAM-GSRTC-DAHOD" in gap["offline"]
    shorts = [s["camera_id"] for s in gap["short_retention"]]
    assert "CAM-FCS-001" in shorts


def test_reject_private_without_consent(client, auth):
    res = client.post(
        "/api/cameras",
        json={
            "camera_id": "CAM-PRIV-X",
            "ownership": "Private-Permitted",
            "consent": False,
            "lat": 23.0,
            "lon": 72.5,
            "location": "mall",
        },
        auth=auth,
    )
    assert res.status_code == 400


def test_sync_without_host_is_400(client, auth):
    res = client.post("/api/cameras/sync-catalogue", auth=auth)
    assert res.status_code == 400
    assert "SENTINEL_HOST" in res.json()["detail"]
