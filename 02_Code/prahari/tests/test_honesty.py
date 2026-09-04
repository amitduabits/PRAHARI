def test_confirm_is_not_labelled_anpr(client, auth):
    res = client.post(
        "/api/ingest/confirm",
        json={"camera_id": "CAM-OWN-001", "plate": "GJ 01 AB 1234"},
        auth=auth,
    )
    assert res.status_code == 200
    event = res.json()["event"]
    assert event["source"] == "operator_confirm"
    assert event["source"] != "anpr"
    assert event["confidence"] == 1.0


def test_footer_keeps_design_target(client):
    text = client.get("/").text
    assert "DESIGN TARGET" in text
    assert "80,000" in text or "80000" in text
