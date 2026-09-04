# C02 — Object detection (person, vehicle, others)

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on C01.

## Goal

A still image yields person/vehicle detections as SQLite rows and a timestamped CSV. CPU only. GPU optional behind a guard.

## Agent

1. `app/services/objects.py`:

```
CLASSES = {"person", "car", "motorcycle", "bus", "truck", "bicycle"}

def detect(frame_bgr) -> list[dict]:
    # each: object_class, confidence, bbox [x,y,w,h], crop_bgr
```

   Backend order:
   - If `OBJECT_ENGINE=yolo` and ultralytics imports, use YOLOv8n.
   - Else if OpenCV DNN weights exist under `app/models_data/` (ONNX or Caffe MobileNet-SSD), use them.
   - Else **fixture fallback**: convert to HSV; a blob occupying ≥ 8% of frame with saturation in a documented range is emitted as `person` with confidence 0.5. This exists so pytest is deterministic without 200 MB weights.
   - Never crash on empty frames. Return [].

2. Generate `tests/fixtures/person_blob.png` with Pillow: 640×360 gray background, a 120×220 skin-tone rectangle (the fallback must detect it). Generate `tests/fixtures/empty_noise.png` random gray.

3. Wire `analyse()` to call `detect` when `objects` in engines. Each object becomes an event: `entity_type=object`, `object_class=...`, `entity_id=object_class`, `plate=""`, `source=objects`.

4. Router `POST /api/ingest/analyse` multipart `file` + `camera_id`. Runs analyse, inserts events, runs matcher. Returns `{events, alerts}`. Keep `POST /api/ingest/frame` as ANPR-only for backward compatibility **or** point it at analyse with engines=anpr only. Document the choice in the router docstring.

5. `GET /api/objects/report.csv` columns: `ts,camera_id,object_class,confidence,event_id,pts_ms`. Auth required.

6. Object track_id: simple IoU tracker in `objects.py` keyed by camera_id. `app.services.capture` scene-cut callback must call `objects.reset(camera_id)`.

7. Tests `tests/test_objects.py` covering T-O01..T-O06 in the catalogue. T-O06: set OBJECT_ENGINE=yolo without the package; detect still returns a list.

## Done when

- pytest includes test_objects and is green.
- Uploading person_blob.png to /api/ingest/analyse as judge inserts ≥1 object row.
- CSV C02-* DONE.

## Do not

Require a GPU. Train a model. Run this as a substitute for ANPR. Store full frames, only crops.
