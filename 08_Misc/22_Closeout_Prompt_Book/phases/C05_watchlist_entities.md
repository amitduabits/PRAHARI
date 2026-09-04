# C05 — Matcher for plates, persons, intrusion

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on C01. Best after C03–C04.

## Goal

`WL-004` (person, empty plate) actually alerts. Intrusion alerts. Plate path unchanged for GJ01AB1234.

## Agent

1. Rewrite `matcher.reload` to index:
   - `_plates: dict[str, row]` non-empty plates
   - `_faces: dict[str, row]` gallery_id or source_case_id for entity_type=person
   - keep 60 s reload behaviour (reload on call if empty is enough for PoC)

2. `on_detection(event)`:
   - if entity_type==intrusion: hit = synthetic {category:INTRUSION, priority:CRITICAL, source_case_id:INTRUSION}
   - elif plate: hit = _plates.get(plate)
   - elif face_id: hit = _faces.get(face_id) or _faces.get(event.entity_id)
   - else: return None (object counts stored, no watchlist card)
   - Dedupe key: (entity_type, entity_id or plate or face_id, camera_id) within 120 s
   - insert_alert must store entity_type and entity_id

3. Extend `tests/test_matcher.py`:
   - existing stolen + dedupe + unknown plate still pass
   - person event face_id=WL-004 → HIGH alert, plate may be empty
   - GJ05CD5678 → HIGH BLACKLIST
   - two intrusion events 10 s apart same camera → one alert, counter=2

4. Optional `tests/test_alerts_ws.py`: TestClient websocket `/ws/alerts`, confirm plate, receive JSON. Skip if starlette websocket setup is painful after 30 minutes; then P1.

5. Watchlist CRUD: POST may include gallery_id, entity_type=person, name. WL-001 still cannot be deleted.

## Done when

- test_matcher.py green and includes person + intrusion cases.
- Boot still seeds GJ01AB1234 CRITICAL from detections.
- CSV C05-* DONE.

## Do not

Match on `name` string equality of “Ramesh K” from OCR. There is no name OCR. Faces go through gallery_id only.
