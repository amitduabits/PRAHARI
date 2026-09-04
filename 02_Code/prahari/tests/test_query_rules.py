"""T-V09: /api/query is keyword_rules, not nlp/llm."""


def test_query_is_keyword_rules(client, auth):
    res = client.post("/api/query", json={"q": "GJ01AB1234 CAM-VAL-001"}, auth=auth)
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["engine"] == "keyword_rules"
    blob = str(body).lower()
    assert "nlp" not in blob
    assert "llm" not in blob
    assert body["filters"].get("plate") == "GJ01AB1234"


def test_query_requires_auth(client):
    res = client.post("/api/query", json={"q": "car"})
    assert res.status_code == 401
