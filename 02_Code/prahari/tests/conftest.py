from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

AUTH = ("judge", "set-this-before-submit")


@pytest.fixture()
def auth():
    return AUTH


@pytest.fixture()
def client(tmp_path, monkeypatch) -> TestClient:
    monkeypatch.setenv("DB_PATH", str(tmp_path / "prahari.db"))
    monkeypatch.setenv("CROP_DIR", str(tmp_path / "crops"))
    monkeypatch.setenv("FACE_DIR", str(tmp_path / "faces"))
    monkeypatch.setenv("JUDGE_PASSWORD", "set-this-before-submit")
    monkeypatch.setenv("FACE_ENGINE", "histogram")
    monkeypatch.setenv("OBJECT_ENGINE", "opencv")
    monkeypatch.setenv("ANPR_ENGINE", "tesseract")
    monkeypatch.setenv("TRACK_ENGINE", "iou")
    monkeypatch.delenv("SENTINEL_HOST", raising=False)
    monkeypatch.delenv("SENTINEL_PASSWORD", raising=False)
    monkeypatch.delenv("SENTINEL_RTSP_HOST", raising=False)
    from app.db import init_db
    from app.main import app

    init_db()
    with TestClient(app) as test_client:
        yield test_client
