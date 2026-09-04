def test_ws_receives_critical(client, auth):
    with client.websocket_connect("/ws/alerts") as ws:
        res = client.post(
            "/api/ingest/confirm",
            json={"camera_id": "CAM-OWN-001", "plate": "GJ01AB1234"},
            auth=auth,
        )
        assert res.status_code == 200
        got = None
        for _ in range(5):
            msg = ws.receive_json()
            if msg.get("type") == "alert":
                got = msg
                break
        assert got is not None
        assert got["alert"]["priority"] in {"CRITICAL", "HIGH"}
