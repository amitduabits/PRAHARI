from app import store


def test_seeded_path(client, auth):
    res = client.get("/api/track/GJ01AB1234", auth=auth)
    assert res.status_code == 200
    body = res.json()
    assert body["count"] >= 6
    ids = [p["camera_id"] for p in body["points"][:6]]
    assert ids == [
        "CAM-VAL-001",
        "CAM-SUR-001",
        "CAM-AHD-004",
        "CAM-AHD-001",
        "CAM-GNR-003",
        "CAM-GNR-001",
    ]
    assert "Valsad" in body["points"][0]["location"]
    csv = client.get("/api/track/GJ01AB1234/report.csv", auth=auth)
    assert csv.status_code == 200
    lines = [ln for ln in csv.text.strip().splitlines() if ln]
    assert len(lines) >= 7


def test_append_does_not_drop_seed(client, auth):
    store.insert_detection(
        {
            "event_id": "extra-rto",
            "plate": "GJ01AB1234",
            "plate_raw": "GJ01AB1234",
            "confidence": 1,
            "camera_id": "CAM-RTO-001",
            "lat": 23.02,
            "lon": 72.57,
            "ts": "2026-08-31T11:00:00+05:30",
            "pts_ms": 0,
            "crop_uri": "",
            "category": "STOLEN",
            "priority": "CRITICAL",
            "source_case_id": "WL-001",
        }
    )
    body = client.get("/api/track/GJ01AB1234", auth=auth).json()
    assert body["count"] >= 7
    assert body["points"][0]["event_id"] == "seed-1"


def test_confirm_new_indian_plate_creates_track(client, auth):
    res = client.post(
        "/api/ingest/confirm",
        json={"camera_id": "CAM-RTO-001", "plate": "GJ27XY0001"},
        auth=auth,
    )
    assert res.status_code == 200
    body = client.get("/api/track/GJ27XY0001", auth=auth).json()
    assert body["count"] >= 1
