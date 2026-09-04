"""Sample own_feed.mp4 at 1 fps for E-A2. Event time is PTS, not wall clock."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault("OPENCV_FFMPEG_CAPTURE_OPTIONS", "rtsp_transport;tcp")

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
sys.path.insert(0, str(ROOT))

import cv2  # noqa: E402

from app.services.anpr import recognize  # noqa: E402
from app.services.capture import detect_scene_cut  # noqa: E402

CLIP = REPO / "03_Data" / "recordings" / "own_feed.mp4"
OUT = REPO / "05_Output" / "experiments" / "own_stills"
LOG = REPO / "05_Output" / "experiments" / "EXPERIMENT_LOG.md"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if not CLIP.is_file():
        row = f"E-A2|{utc}|MEASURED|false|true|skip_reason=own_feed.mp4 missing"
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a", encoding="utf-8") as handle:
            handle.write(row + "\n")
        print(row)
        return 0
    cap = cv2.VideoCapture(str(CLIP))
    kept = 0
    prev = None
    last_keep = -10_000
    plates = []
    while kept < 8:
        ok, frame = cap.read()
        if not ok:
            break
        pts = int(cap.get(cv2.CAP_PROP_POS_MSEC) or 0)
        detect_scene_cut(prev, pts)
        prev = pts
        if pts - last_keep < 1000:
            continue
        last_keep = pts
        dest = OUT / f"t{kept:02d}_{pts}ms.jpg"
        cv2.imwrite(str(dest), frame)
        try:
            result = recognize(frame)
            plates.append({"pts_ms": pts, "plate": result.get("plate"), "confidence": result.get("confidence")})
        except Exception as exc:
            plates.append({"pts_ms": pts, "error": str(exc), "skipped": True})
        kept += 1
    cap.release()
    payload = {
        "id": "E-A2",
        "utc": utc,
        "label": "MEASURED",
        "ok": True,
        "skipped": False,
        "metrics": {"frames": kept, "plates": plates},
    }
    (REPO / "05_Output" / "experiments" / f"E-A2_{utc.replace(':', '')}.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(f"E-A2|{utc}|MEASURED|true|false|frames={kept}\n")
    print(json.dumps(payload["metrics"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
