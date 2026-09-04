from app.services import matcher


def test_stolen_and_dedupe_and_unknown(client):
    matcher.reload()
    row = matcher.match("GJ01AB1234")
    assert row is not None
    assert row["priority"] == "CRITICAL"

    first = matcher.on_detection(
        {
            "event_id": "t1",
            "plate": "GJ01AB1234",
            "camera_id": "CAM-VAL-001",
            "ts": "2026-08-31T06:12:10+05:30",
        },
        notify=False,
    )
    assert first is not None
    counter = first["counter"]
    second = matcher.on_detection(
        {
            "event_id": "t2",
            "plate": "GJ01AB1234",
            "camera_id": "CAM-VAL-001",
            "ts": "2026-08-31T06:12:20+05:30",
        },
        notify=False,
    )
    assert second["alert_id"] == first["alert_id"]
    assert second["counter"] == counter + 1

    later = matcher.on_detection(
        {
            "event_id": "t3",
            "plate": "GJ01AB1234",
            "camera_id": "CAM-VAL-001",
            "ts": "2026-08-31T06:15:00+05:30",
        },
        notify=False,
    )
    assert later["alert_id"] != first["alert_id"]

    none = matcher.on_detection(
        {"event_id": "t4", "plate": "XX99YY9999", "camera_id": "CAM-VAL-001", "ts": "2026-08-31T11:00:00+05:30"},
        notify=False,
    )
    assert none is None


def test_person_face_id_without_plate():
    from app.services import matcher

    matcher.reload()
    hit = matcher.on_detection(
        {
            "event_id": "face-1",
            "entity_type": "person",
            "face_id": "WL-004",
            "entity_id": "WL-004",
            "plate": "",
            "camera_id": "CAM-OWN-001",
            "ts": "2026-08-31T12:00:00+05:30",
        },
        notify=False,
    )
    assert hit is not None
    assert hit["priority"] == "HIGH"
    assert hit.get("entity_type") == "person"


def test_blacklist_plate_is_high():
    from app.services import matcher

    matcher.reload()
    hit = matcher.on_detection(
        {
            "event_id": "bl-1",
            "plate": "GJ05CD5678",
            "camera_id": "CAM-AHD-001",
            "ts": "2026-08-31T12:30:00+05:30",
        },
        notify=False,
    )
    assert hit is not None
    assert hit["priority"] == "HIGH"
    assert hit["category"] == "BLACKLIST"
