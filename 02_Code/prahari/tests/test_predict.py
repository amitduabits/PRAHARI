"""T-V08: GET /api/predict/GJ01AB1234 returns a list; never 500."""


def test_predict_seeded_plate(client, auth):
    res = client.get("/api/predict/GJ01AB1234", auth=auth)
    assert res.status_code == 200, res.text
    body = res.json()
    assert "predictions" in body
    assert isinstance(body["predictions"], list)


def test_predict_requires_auth(client):
    res = client.get("/api/predict/GJ01AB1234")
    assert res.status_code == 401


def test_predict_one_point_does_not_500(client, auth):
    from app import store

    store.insert_detection(
        {
            "event_id": "pred-one",
            "plate": "GJ99ZZ0001",
            "camera_id": "CAM-VAL-001",
            "lat": 20.6,
            "lon": 72.9,
            "ts": "2026-08-31T06:00:00+05:30",
        }
    )
    res = client.get("/api/predict/GJ99ZZ0001", auth=auth)
    assert res.status_code == 200
    assert isinstance(res.json()["predictions"], list)
