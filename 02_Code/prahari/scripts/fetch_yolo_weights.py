"""Download yolov8n.pt into app/models_data/. Not run by pytest."""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "app" / "models_data" / "yolov8n.pt"
URL = "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt"


def main() -> int:
    DEST.parent.mkdir(parents=True, exist_ok=True)
    if DEST.is_file() and DEST.stat().st_size > 1_000_000:
        print("already present", DEST)
        return 0
    print("downloading", URL)
    urllib.request.urlretrieve(URL, DEST)
    print("wrote", DEST, "bytes", DEST.stat().st_size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
