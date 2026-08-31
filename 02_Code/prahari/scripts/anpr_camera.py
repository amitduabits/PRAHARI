from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("OPENCV_FFMPEG_CAPTURE_OPTIONS", "rtsp_transport;tcp")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db import init_db
from app.paths import capture_url
from app.services.anpr import recognize
from app.services.capture import StreamSession
from app.services.sampler import sample_frames
from app import store


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera-id", default="CAM-OWN-001")
    parser.add_argument("--seconds", type=int, default=15)
    args = parser.parse_args()
    init_db()
    cam = store.get_camera(args.camera_id)
    if not cam:
        print("unknown camera", file=sys.stderr)
        return 2
    url, protocol = capture_url(cam)
    if protocol == "file" and not Path(url).is_file():
        print(f"file missing: {url}", file=sys.stderr)
        return 2
    session = StreamSession()
    try:
        session.open(url, protocol)
        seen = 0
        for frame, pts in sample_frames(session):
            result = recognize(frame)
            print(pts, result.get("plate"), result.get("plate_raw"), result.get("confidence"))
            seen += 1
            if seen * 1 >= args.seconds:
                break
    finally:
        session.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
