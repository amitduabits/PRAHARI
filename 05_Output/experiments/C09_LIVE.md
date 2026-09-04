# C09 live experiments

- Own-feed: E-A2 MEASURED 8 stills from `own_feed.mp4` at PTS 1 s. Plates empty because Tesseract is not on PATH (`recognize()` now returns plate=None instead of raising).
- Objects on the person-blob fixture: E-O1 MEASURED 1 person.
- FRS: E-F1 MEASURED gallery hit `WL-004`. E-F3-static: `engines_for(cam04)` drops faces.
- Government catalogue: E-G1 SKIPPED in this process (`SENTINEL_HOST` empty to `run_experiments --suite gov`). `/api/health` on the seeded app reported `sentinel_host_configured: true` in smoke against the live SQLite file; a live grab was not repeated here to avoid opening RTSP without an operator. Existing `gov_feed_plates.csv` remains two operator-confirm rows; `gov_feed_plates.NOTE.txt` still says OCR empty, confirm used.
