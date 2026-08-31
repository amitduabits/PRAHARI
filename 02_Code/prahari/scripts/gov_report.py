from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db import init_db
from app import config, store

OUT = config.REPO_ROOT / "05_Output" / "deliverables" / "gov_feed_plates.csv"
NOTE = config.REPO_ROOT / "05_Output" / "deliverables" / "gov_feed_plates.NOTE.txt"


def main() -> None:
    init_db()
    cams = {c["camera_id"]: c for c in store.list_cameras()}
    catalogue_ids = {cid for cid, c in cams.items() if (c.get("department") == "Sentinel" or c.get("cam_type") == "sandbox")}
    rows = store.list_detections()
    selected = [r for r in rows if r["camera_id"] in catalogue_ids]
    confirm_used = any(r.get("confidence") == 1.0 for r in selected)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["plate", "camera_id", "ts", "confidence", "category"])
        writer.writeheader()
        for r in selected:
            writer.writerow(
                {
                    "plate": r.get("plate"),
                    "camera_id": r.get("camera_id"),
                    "ts": r.get("ts"),
                    "confidence": r.get("confidence"),
                    "category": r.get("category"),
                }
            )
    if not selected:
        NOTE.write_text("OCR empty, confirm used" if confirm_used else "No catalogue detections yet. SENTINEL_HOST empty or no live ANPR hits.\n", encoding="utf-8")
    elif confirm_used and all((r.get("confidence") or 0) >= 1 for r in selected):
        NOTE.write_text("OCR empty, confirm used\n", encoding="utf-8")
    print(OUT, "rows", len(selected))


if __name__ == "__main__":
    main()
