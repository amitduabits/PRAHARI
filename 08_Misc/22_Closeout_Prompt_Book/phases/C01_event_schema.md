# C01 — Additive event schema

Prepend `00_MASTER_CONTEXT.md`. AGENT. Read `04_ANALYTICS_CONTRACT.md`.

## Goal

Detection events can describe plates, faces, objects, and intrusion without breaking GJ01AB1234.

## Agent

1. In `app/db.py` `SCHEMA` and a migration helper run from `init_db()`: `ALTER TABLE ... ADD COLUMN` for each new field if missing. SQLite ignores duplicate-add if you catch OperationalError “duplicate column”.

   detections: `entity_type TEXT DEFAULT 'vehicle'`, `entity_id TEXT`, `face_id TEXT`, `object_class TEXT`, `bbox_json TEXT`, `track_id TEXT`, `source TEXT DEFAULT ''`

   alerts: `entity_type TEXT`, `entity_id TEXT`

   watchlist: `gallery_id TEXT`, `embedding_uri TEXT`

2. Extend `app/models.py` `DETECTION_COLUMNS`. Keep the frozen plate fields first.

3. `store.insert_detection` must accept extra keys and default `entity_type='vehicle'`, `entity_id=plate`, `source=''`. Seeded detections keep working.

4. Add `app/services/analyse.py`:

```
def engines_for(camera: dict) -> list[str]:
    # env ANALYTICS_ENGINES default anpr,objects
    # drop 'faces' if camera_id matches ^cam\d+ or ownership in {Gov, Private-Permitted}

def analyse(frame_bgr, camera: dict, pts_ms: int = 0) -> list[dict]:
    # call recognize / objects.detect / faces.match / intrusion.check when those modules exist
    # if a module is missing, skip that engine
```

   For C01, objects/faces/intrusion may still be missing: analyse runs ANPR only and returns a list of zero or one event dicts (not inserted).

5. Tests `tests/test_event_schema.py`:
   - init_db on tmp db; PRAGMA table_info detections contains entity_type and plate.
   - insert_detection with only the old keys succeeds.
   - GET /api/track/GJ01AB1234 still count ≥ 6.
   - engines_for({'camera_id':'cam04','ownership':'Gov'}) does not include faces.
   - engines_for({'camera_id':'CAM-OWN-001','ownership':'Own'}) includes faces if ANALYTICS_ENGINES lists faces.

6. All previous tests stay green.

## Done when

- `pytest -q tests/test_event_schema.py tests/test_track.py tests/test_matcher.py` green.
- CSV C01-* DONE.

## Do not

Rename plate fields. Drop seed rows. Run FRS on cam04.
