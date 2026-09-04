# C09 — Own-feed and government-feed experiments

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on C08. HUMAN: SENTINEL_HOST already in .env from W01.

## Goal

MEASURED evidence for official demos 3 and 4, including object analytics on gov frames and FRS **refuse** on gov frames.

## Agent

1. Own-feed:
   - Ensure `03_Data/recordings/own_feed.mp4` plays via CAM-OWN-001.
   - Run E-A2, E-O2, E-O4, E-F1. If consented photos exist, E-F2; else SKIPPED.
   - POST analyse a still from the mp4 as judge. Log event counts by entity_type.

2. Government:
   - If SENTINEL_HOST empty: write SKIPPED for E-G* and stop that half.
   - Else: sync-catalogue; update `onboard_failures.md`; grab cam04 JPEG; recognize (honest none); detect objects; **force** ANALYTICS_ENGINES=anpr,objects,faces and assert face events == 0 (E-F3, E-X4).
   - Regenerate `05_Output/deliverables/gov_feed_plates.csv` from detections where camera_id like `cam%` and plate non-empty. Keep `gov_feed_plates.NOTE.txt` stating anpr vs operator_confirm counts.
   - If objects exist, write `gov_feed_objects.csv` with timestamps.

3. Do not wget `/stream/<id>`. Use grab_frame.py (TCP) or HLS fallback already in capture.py.

4. Append all runs to EXPERIMENT_LOG.md.

## Done when

- Own-feed experiments logged.
- Gov half logged as MEASURED or SKIPPED.
- Face count on cam04 is 0.
- CSV C09-* DONE.

## Do not

Enroll Paldi Circle faces. Claim OCR if recognize returned None. Open more than two live RTSP sessions.
