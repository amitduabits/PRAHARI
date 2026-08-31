def test_list_and_one_have_no_rtsp(client, auth):
    listing = client.get("/api/cameras", auth=auth)
    assert listing.status_code == 200
    assert "rtsp://" not in listing.text
    one = client.get("/api/cameras/CAM-VAL-001", auth=auth)
    assert one.status_code == 200
    assert "rtsp://" not in one.text
    assert "playback" in one.json()
