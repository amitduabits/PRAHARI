from __future__ import annotations

from app.db import connect, init_db
from app.services.analyse import engines_for


def test_detections_have_additive_columns():
    init_db()
    cols = {row[1] for row in connect().execute("PRAGMA table_info(detections)")}
    assert "plate" in cols
    assert "entity_type" in cols
    assert "face_id" in cols
    assert "object_class" in cols
    assert "source" in cols


def test_old_insert_keys_still_work(client, auth):
    from app import store

    store.insert_detection(
        {
            "event_id": "schema-old",
            "plate": "GJ27XY0001",
            "plate_raw": "GJ27XY0001",
            "confidence": 1,
            "camera_id": "CAM-RTO-001",
            "lat": 23.02,
            "lon": 72.57,
            "ts": "2026-08-31T12:00:00+05:30",
            "pts_ms": 0,
            "crop_uri": "",
            "category": "OBSERVE",
            "priority": "LOW",
            "source_case_id": "WL-005",
        }
    )
    body = client.get("/api/track/GJ01AB1234", auth=auth).json()
    assert body["count"] >= 6


def test_engines_for_drops_faces_on_gov(monkeypatch):
    monkeypatch.setenv("ANALYTICS_ENGINES", "anpr,objects,faces")
    gov = engines_for({"camera_id": "cam04", "ownership": "Gov"})
    assert "faces" not in gov
    own = engines_for({"camera_id": "CAM-OWN-001", "ownership": "Own"})
    assert "faces" in own
