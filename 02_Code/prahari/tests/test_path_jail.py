from pathlib import Path

from app.auth import issue_stream_token


def test_jail_file_url_does_not_stream_os_file(client, auth):
    res = client.post(
        "/api/cameras",
        json={
            "camera_id": "CAM-JAIL",
            "lat": 23.0,
            "lon": 72.0,
            "consent": True,
            "protocol": "file",
            "url": "../../../../Windows/win.ini",
        },
        auth=auth,
    )
    assert res.status_code == 200
    one = client.get("/api/cameras/CAM-JAIL", auth=auth)
    assert one.status_code == 200
    token = one.json()["playback"]["token"]
    streamed = client.get("/api/stream/CAM-JAIL", params={"token": token})
    assert streamed.status_code in {400, 404}
    assert b"[extensions]" not in streamed.content.lower()
    assert b"for 16-bit app support" not in streamed.content.lower()


def test_own_feed_still_in_media_root(client, auth):
    one = client.get("/api/cameras/CAM-OWN-001", auth=auth)
    assert one.status_code == 200
    token = one.json()["playback"]["token"]
    streamed = client.get("/api/stream/CAM-OWN-001", params={"token": token})
    own = Path(__file__).resolve().parents[3] / "03_Data" / "recordings" / "own_feed.mp4"
    if own.is_file():
        assert streamed.status_code == 200
    else:
        assert streamed.status_code == 404
        assert "own_feed.mp4" in streamed.json()["detail"]


def test_issue_token_helper_exists():
    token = issue_stream_token("CAM-OWN-001", "judge")
    assert token.count("|") == 3
