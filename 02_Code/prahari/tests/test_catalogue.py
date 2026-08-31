from app.services.catalogue import load_fixture, parse_payload


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
