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
