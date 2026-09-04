"""Live capture. Integrator laws: TCP, PTS, backoff, non-fatal decode, pace load."""

from __future__ import annotations

import logging
import os

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"

import time  # reconnect scheduler only; event time is PTS, never time.time()
from typing import Any, Callable

import cv2

from app import config

log = logging.getLogger("prahari.capture")

RECONNECT_MIN_S = config.RECONNECT_MIN_S
RECONNECT_MAX_S = config.RECONNECT_MAX_S
SCENE_CUT_GAP_MS = 5000

_OPEN: dict[int, "StreamSession"] = {}


def backoff_sleep(attempt: int) -> float:
    """Wall clock used only to space reconnects, never as an event timestamp."""
    delay = min(RECONNECT_MIN_S * (2 ** attempt), RECONNECT_MAX_S)
    time.sleep(delay)
    return delay


def detect_scene_cut(prev_pts: int | None, pts: int, gap_ms: int = SCENE_CUT_GAP_MS) -> bool:
    if prev_pts is None:
        return False
    if pts < prev_pts:
        return True
    if pts - prev_pts > gap_ms:
        return True
    return False


def _reset_trackers(camera_id: str) -> None:
    try:
        from app.services import objects as objects_mod

        objects_mod.reset(camera_id)
    except Exception:
        pass
    try:
        from app.services import faces as faces_mod

        faces_mod.reset(camera_id)
    except Exception:
        pass


class StreamSession:
    def __init__(self, on_scene_cut: Callable[[], None] | None = None, camera_id: str = "") -> None:
        self.cap: cv2.VideoCapture | None = None
        self.url = ""
        self.protocol = ""
        self.camera_id = camera_id
        self.on_scene_cut = on_scene_cut
        self.prev_pts: int | None = None
        self.reconnects = 0
        self._id = id(self)

    def open(self, url: str, protocol: str = "rtsp", camera_id: str = "") -> None:
        max_open = config.MAX_OPEN_CAPTURES
        if self._id not in _OPEN and len(_OPEN) >= max_open:
            raise RuntimeError(
                f"MAX_OPEN_CAPTURES={max_open} reached. Close an idle capture before opening another."
            )
        self.url = url
        self.protocol = protocol
        if camera_id:
            self.camera_id = camera_id
        self._open_cap()
        _OPEN[self._id] = self

    def _open_cap(self) -> None:
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
        if not cap.isOpened():
            cap.release()
            raise RuntimeError(f"cannot open {self.protocol} url")
        self.cap = cap
        self.prev_pts = None

    def read(self, reconnect: bool = True) -> tuple[bool, Any, int]:
        if self.cap is None:
            return False, None, 0
        attempt = 0
        while True:
            try:
                ok, frame = self.cap.read()
            except cv2.error as exc:
                log.warning("decode warning at join (non-fatal): %s", exc)
                ok, frame = False, None
            if ok and frame is not None:
                pts_ms = int(self.cap.get(cv2.CAP_PROP_POS_MSEC) or 0)
                if detect_scene_cut(self.prev_pts, pts_ms):
                    log.info("scene cut at pts_ms=%s prev=%s", pts_ms, self.prev_pts)
                    if self.on_scene_cut:
                        self.on_scene_cut()
                    _reset_trackers(self.camera_id)
                self.prev_pts = pts_ms
                return True, frame, pts_ms
            if not reconnect:
                return False, None, 0
            self.reconnects += 1
            delay = backoff_sleep(attempt)
            attempt += 1
            log.warning("capture gap/fail, reconnect in %ss (%s)", delay, self.url)
            try:
                self._open_cap()
            except Exception as exc:
                log.warning("reconnect failed: %s", exc)

    def close(self) -> None:
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        _OPEN.pop(self._id, None)

    def __enter__(self) -> "StreamSession":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


def open_count() -> int:
    return len(_OPEN)
