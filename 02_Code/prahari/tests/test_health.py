def test_health_seed_counts(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["cameras"] >= 11
    assert body["detections"] >= 6
    assert body["watchlist"] >= 5
    assert body["sentinel_host_configured"] is False


def test_index_shell(client):
    response = client.get("/")
    assert response.status_code == 200
    text = response.text
    assert "PRAHARI" in text
    assert "Operations" in text
    assert "Vehicle Track" in text
    assert "lorem" not in text.lower()
