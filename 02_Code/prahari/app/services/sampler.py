"""1 fps sampling driven by PTS deltas. Ignore declared frame-rate properties. Do not sleep(1) as 1 fps."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from app.services.capture import StreamSession

# When a file source reports PTS=0, keep every Nth frame and synthesise pts_ms = kept * 1000.
# N=25 is a documented stand-in for a typical 25 fps file, not a reading of the capture FPS property.
FILE_PTS_MISSING_N = 25


def sample_frames(session: StreamSession, min_delta_ms: int = 1000) -> Iterator[tuple[Any, int]]:
    last_pts: int | None = None
    n = 0
    kept = 0
    while True:
        ok, frame, pts_ms = session.read(reconnect=True)
        if not ok:
            break
        n += 1
        if pts_ms == 0:
            if n % FILE_PTS_MISSING_N != 1:
                continue
            kept += 1
            yield frame, kept * 1000
            continue
        if last_pts is None or pts_ms - last_pts >= min_delta_ms:
            last_pts = pts_ms
            yield frame, pts_ms
