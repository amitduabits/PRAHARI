from app.services.catalogue import apply_origin_urls, load_fixture, parse_payload


def test_fixture_three_cameras_mixed_codec():
    cams = load_fixture()
    assert len(cams) == 3
    codecs = {c["codec"] for c in cams}
    assert "h264" in codecs and "h265" in codecs
    assert any(c["width"] == 1280 and c["height"] == 720 for c in cams)
    assert any(c["live"] is False for c in cams)
    assert any(c["id"] == "1" for c in cams)
    assert any(c["id"] == "2" for c in cams)


def test_hlsurl_alias():
    payload = {
        "cameras": [
            {"Id": 9, "HlsUrl": "http://example/live/stream/9/index.m3u8", "codec": "h264"}
        ]
    }
    cams = parse_payload(payload)
    assert cams[0]["id"] == "9"
    assert cams[0]["hls"].endswith("index.m3u8")


def test_urls_come_from_json_not_constructed():
    src = (load_fixture()[0]["rtsp"])
    assert src.startswith("rtsp://")
    from pathlib import Path
    text = Path(__file__).resolve().parents[1].joinpath("app/services/catalogue.py").read_text(encoding="utf-8")
    assert "rtsp://{host" not in text
    assert "rtsp://<" not in text


def test_live_manifest_id_and_name():
    payload = [
        {"id": "cam04", "name": "04 Paldi Circle"},
        {"id": "cam01", "name": "01 Chiman bhai Bridge"},
    ]
    cams = parse_payload(payload)
    assert [c["id"] for c in cams] == ["cam04", "cam01"]
    assert cams[0]["location"] == "04 Paldi Circle"
    assert cams[0]["live"] is True
    assert cams[0]["hls"] == ""
    assert cams[0]["rtsp"] == ""


def test_apply_origin_urls_fills_missing_only():
    cam = {
        "id": "cam04",
        "location": "04 Paldi Circle",
        "codec": "",
        "live": True,
        "width": 0,
        "height": 0,
        "fps_declared": 0.0,
        "rtsp": "",
        "whep": "",
        "hls": "",
        "raw": {},
    }
    filled = apply_origin_urls(cam, "https://cctv.corp8.cloud", "103.250.160.189")
    assert filled["hls"] == "https://cctv.corp8.cloud/cam04/index.m3u8"
    assert filled["rtsp"] == "rtsp://103.250.160.189:8554/stream/cam04"
    assert filled["whep"].endswith("/stream/cam04/whep")
    kept = apply_origin_urls(
        {**cam, "hls": "http://example/live/x.m3u8", "rtsp": "rtsp://example/stream/9"},
        "https://cctv.corp8.cloud",
        "103.250.160.189",
    )
    assert kept["hls"] == "http://example/live/x.m3u8"
    assert kept["rtsp"] == "rtsp://example/stream/9"
