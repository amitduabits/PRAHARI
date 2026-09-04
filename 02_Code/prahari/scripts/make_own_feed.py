"""Synthetic own-feed clip so the demo tile has a file. Replace with a consented road clip when it exists."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "03_Data" / "recordings" / "own_feed.mp4"
W, H, FPS, SECONDS = 1280, 720, 15, 130


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(OUT), fourcc, FPS, (W, H))
    if not writer.isOpened():
        raise SystemExit("VideoWriter failed")
    for i in range(FPS * SECONDS):
        frame = np.full((H, W, 3), 32, dtype=np.uint8)
        x = 360 + int(40 * np.sin(i / 18.0))
        y = 280 + int(12 * np.cos(i / 22.0))
        cv2.rectangle(frame, (x, y), (x + 560, y + 160), (240, 240, 240), -1)
        cv2.rectangle(frame, (x, y), (x + 560, y + 160), (20, 20, 20), 4)
        cv2.putText(
            frame,
            "GJ01AB1234",
            (x + 40, y + 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            2.2,
            (10, 10, 10),
            5,
            cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            "PRAHARI own-feed stand-in  CAM-OWN-001",
            (40, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (200, 200, 200),
            2,
            cv2.LINE_AA,
        )
        writer.write(frame)
    writer.release()
    print(OUT, "bytes", OUT.stat().st_size)


if __name__ == "__main__":
    main()
