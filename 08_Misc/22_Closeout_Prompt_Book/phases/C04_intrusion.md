# C04 — Godown intrusion (person in ROI)

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on C02.

## Goal

Food & Civil Supplies camera `CAM-FCS-001` raises a CRITICAL intrusion when a person box overlaps a stored ROI. This is the eval-05 intrusion item.

## Agent

1. `app/services/intrusion.py`:

```
def roi_of(camera: dict) -> list[list[float]] | None
def check(frame_bgr, camera: dict, object_events: list[dict]) -> dict | None
```

   ROI is `json.loads(camera['extra_json']).get('roi')` as list of [x,y] normalised 0–1, or pixel box `[x0,y0,x1,y1]`. IoU or intersection-over-person-area ≥ 0.30 fires.

2. Seed ROI for CAM-FCS-001 in extra_json: full lower half of the frame `[[0,0.5],[1,0.5],[1,1],[0,1]]` so the person_blob fixture (centred) can be placed accordingly. For tests, build a camera dict; do not break existing seed if extra_json is empty — check() returns None.

3. Event: `entity_type=intrusion`, `entity_id=CAM-FCS-001`, `category=INTRUSION`, `priority=CRITICAL`, `object_class=person`, `source=intrusion`. Matcher in C05 will treat intrusion as always-alert. For C04, insert_alert directly if matcher does not yet understand intrusion, **or** call matcher with the event.

4. Tests `tests/test_intrusion.py` T-I01..T-I04. Use a synthetic frame and a camera dict; do not require the sandbox.

5. Scene-cut: no special state other than object tracker reset.

## Done when

- test_intrusion.py green.
- CSV C04-* DONE.

## Do not

New neural net. Motion-only without a person class if objects.py already emits person. Alert on every frame without 120 s dedupe.
