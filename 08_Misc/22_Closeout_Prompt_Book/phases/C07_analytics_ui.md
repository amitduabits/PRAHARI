# C07 — Analytics UI

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on C02, C03, C05.

## Goal

A judge clicking Onboard and Analytics sees plates, objects, optional own-feed face match, and intrusion counts. Person alerts show a name, not a blank plate.

## Agent

1. `static/index.html` Onboard section: add “Analyse this still” file input posting `/api/ingest/analyse`. Keep ANPR-only and Confirm plate. Add Confirm face (camera_id + gallery_id) posting `/api/ingest/confirm-face`.

2. `static/app.js`:
   - Render analyse result: plate, list of object_class+confidence, face_id+name, intrusion flag.
   - Alerts: if entity_type==person, title is `name or face_id`; if intrusion, title `INTRUSION @ camera_id`; else plate.
   - Analytics & Gaps: after gap JSON, fetch detections grouped by entity_type; link to `/api/objects/report.csv`.

3. Watchlist table: show entity_type, plate, name, gallery_id.

4. `tests/test_tabs_smoke.py` still 200. Add a light test that GET / contains the string `Analyse this still`.

5. Honest empty states. No lorem. No “NAFIS live”.

## Done when

- Click-tour of seven tabs does not 500.
- Analyse still on CAM-OWN-001 with person_blob.png shows an object line.
- CSV C07-* DONE.

## Do not

Eighth top-level tab unless necessary. FRS button on a flow that uses cam04. Leaflet CDN change.
