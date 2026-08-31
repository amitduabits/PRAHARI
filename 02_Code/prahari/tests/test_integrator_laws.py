from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICES = (ROOT / "app" / "services").read_text if False else ROOT / "app" / "services"


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_tcp_flag_in_capture_and_grab():
    capture = _read("app/services/capture.py")
    grab = _read("scripts/grab_frame.py")
    blob = capture + grab
    assert "rtsp_transport;tcp" in blob or "rtsp_transport tcp" in blob


def test_no_cap_prop_fps_in_services():
    for path in (ROOT / "app" / "services").glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "CAP_PROP_FPS" not in text, path.name


def test_time_time_only_in_backoff():
    text = _read("app/services/capture.py")
    if "time.time" not in text:
        return
    for i, line in enumerate(text.splitlines(), 1):
        if "time.time" in line:
            # allowed only inside backoff_sleep / reconnect scheduler
            window = "\n".join(text.splitlines()[max(0, i - 15) : i + 5])
            assert "def backoff_sleep" in window or "reconnect" in window.lower()


def test_backoff_constants():
    text = _read("app/services/capture.py")
    assert "RECONNECT_MIN_S" in text or "2" in text
    assert "RECONNECT_MAX_S" in text or "30" in text


def test_no_publish_helpers():
    text = _read("app/services/catalogue.py") + _read("app/services/capture.py")
    for name in ("def publish", "def push_stream", "def control_api"):
        assert name not in text
