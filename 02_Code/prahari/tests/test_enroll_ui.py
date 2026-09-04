"""T-V10: Watchlist Enroll form exists; viewer still 403."""


def test_index_contains_enroll(client):
    text = client.get("/").text
    assert "Enroll" in text
    assert "Enroll Missing/Wanted Person" in text


def test_viewer_enroll_403(client):
    res = client.post(
        "/api/faces/enroll",
        data={"gallery_id": "WL-004", "name": "nope"},
        files={"file": ("x.png", b"xxxx", "image/png")},
        auth=("home.viewer", "viewer"),
    )
    assert res.status_code == 403
