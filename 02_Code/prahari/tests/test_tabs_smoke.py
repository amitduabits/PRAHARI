def test_index_and_core_apis(client, auth):
    index = client.get("/")
    assert index.status_code == 200
    text = index.text.lower()
    assert "lorem" not in text
    assert "todo" not in text
    assert "tbd" not in text
    assert "analyse this still" in text
    for path in (
        "/api/health",
        "/api/cameras",
        "/api/alerts?status=open",
        "/api/watchlist",
        "/api/track/GJ01AB1234",
        "/api/predict/GJ01AB1234",
        "/api/gap-report",
        "/api/detections",
    ):
        kwargs = {} if path == "/api/health" else {"auth": auth}
        res = client.get(path, **kwargs)
        assert res.status_code == 200, path
