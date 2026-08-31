"""Grab one JPEG. Forces RTSP over TCP via capture.py (OPENCV_FFMPEG_CAPTURE_OPTIONS=rtsp_transport;tcp)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("OPENCV_FFMPEG_CAPTURE_OPTIONS", "rtsp_transport;tcp")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import cv2  # noqa: E402

from app.db import init_db  # noqa: E402
from app.paths import capture_url  # noqa: E402
from app.services.capture import StreamSession  # noqa: E402
from app import store  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera-id")
    parser.add_argument("--url")
    parser.add_argument("--protocol", default="file", choices=["file", "rtsp", "hls"])
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    init_db()
    protocol = args.protocol
    url = args.url or ""
    camera_id = args.camera_id or "grab"
    if args.camera_id:
        cam = store.get_camera(args.camera_id)
        if not cam:
            print(f"unknown camera {args.camera_id}", file=sys.stderr)
            return 2
        url, protocol = capture_url(cam)
        camera_id = cam["camera_id"]
    if protocol == "file" and url and not Path(url).is_file():
        print(f"file missing: {url}", file=sys.stderr)
        return 2
    if not url:
        print("no url", file=sys.stderr)
        return 2
    session = StreamSession()
    try:
        session.open(url, protocol)
        ok, frame, pts_ms = session.read(reconnect=False)
    except Exception as exc:
        print(f"open failed: {exc}", file=sys.stderr)
        return 2
    finally:
        session.close()
    if not ok or frame is None:
        print("no frame", file=sys.stderr)
        return 2
    out = Path(args.out) if args.out else ROOT / "data" / "crops" / f"{camera_id}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out), frame)
    print(f"wrote {out} pts_ms={pts_ms}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
