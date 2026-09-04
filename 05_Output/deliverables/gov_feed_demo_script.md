# Gov-feed demo script (≤3 min)

Camera on http://127.0.0.1:8080. Login `judge`. No `.env` on screen. No RTSP URL on screen.

| Sec | Click | Say |
|---|---|---|
| 0:00–0:20 | Cameras table, Sentinel rows | MUST: Live catalogue from cameras.json. Thirty cameras. No coordinates in that JSON. |
| 0:20–0:40 | Open tile on cam04 from the table | MUST: We open Paldi Circle from the table, not from a map pin. The live catalogue has no GIS. |
| 0:40–1:10 | Tile playing (HLS) | Live HLS through a tokenised proxy. Raw RTSP never reaches the browser. If 8554 is blocked we stay on HLS. |
| 1:10–1:35 | Onboard confirm GJ01AB1234 on cam04 | MUST unless a new OCR row exists: This row is operator confirm, confidence one, not ANPR. Tesseract was not on PATH when we measured. |
| 1:35–1:55 | Analyse this still on cam04 | Objects if the detector fires. MUST: we do not run FRS on this feed. |
| 1:55–2:15 | Vehicle Track Reconstruct | MUST: Live confirm appended. The six seed points are still there. |
| 2:15–2:40 | Download CSV | MUST: Government output report. Plate, camera cam04, timestamp, stolen. Object CSV if rows exist. |
| 2:40–3:00 | Alerts CRITICAL | Representative watchlist match. Stolen is CRITICAL. |
