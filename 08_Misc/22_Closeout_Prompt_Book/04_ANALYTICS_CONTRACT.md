# Analytics contract (closeout)

This is the interface freeze for C01–C07. Agents must not invent a second pipeline.

## 1. One analyse() entry

`app/services/analyse.py`

```
def analyse(frame_bgr, camera: dict, pts_ms: int) -> list[dict]:
    """Run enabled engines. Return zero or more detection events (not yet inserted)."""
```

Enabled engines from env (comma list), default:

```
ANALYTICS_ENGINES=anpr,objects
```

On `CAM-OWN-001` (own-feed, enrolled gallery present):

```
ANALYTICS_ENGINES=anpr,objects,faces
```

On government catalogue cameras (`cam01` …):

```
ANALYTICS_ENGINES=anpr,objects
```

`faces` is refused if `camera["ownership"]` is not `Own` **or** if `camera_id` matches `^cam\d+`. Write a test for that refuse.

Godown `CAM-FCS-001` additionally runs intrusion (person-in-ROI). Intrusion is a wrapper on objects, not a fourth neural net.

## 2. Engines

| Module | Function | Output fields | Default backend | Swap |
|---|---|---|---|---|
| `anpr.py` | `recognize(frame)` | plate, plate_raw, confidence, crop_bgr, box | OpenCV morph + Tesseract | YOLO plate + PaddleOCR |
| `objects.py` | `detect(frame)` | list of {object_class, confidence, bbox, crop_bgr} | OpenCV DNN CPU (COCO: person, car, motorcycle, bus, truck, bicycle) | YOLOv8n if `OBJECT_ENGINE=yolo` |
| `faces.py` | `match(frame, gallery)` | list of {face_id, confidence, bbox, crop_bgr} or unmatched | OpenCV face detect + LBPH | insightface if `FACE_ENGINE=insightface` |
| `intrusion.py` | `check(frame, camera, objects)` | event if person bbox IoU with ROI ≥ 0.30 | ROI from `cameras.extra_json` | none |

No engine may import `cv2` before `OPENCV_FFMPEG_CAPTURE_OPTIONS` is set. Object and face trackers reset on scene cut.

## 3. Schema additions (additive)

`detections` new columns (SQLite `ALTER TABLE` if missing, keep old columns):

```
entity_type TEXT DEFAULT 'vehicle'
entity_id   TEXT
face_id     TEXT
object_class TEXT
bbox_json   TEXT
track_id    TEXT
```

`alerts` new columns:

```
entity_type TEXT
entity_id   TEXT
```

`watchlist` already has `entity_type`, `plate`, `name`. Add:

```
gallery_id  TEXT
embedding_uri TEXT
```

`WL-001` remains plate `GJ01AB1234`. `WL-004` is `entity_type=person`, `gallery_id=WL-004`. Matcher must fire on `face_id=WL-004`, not on an empty plate.

Crops:

```
data/crops/{camera_id}/{event_id}.jpg
data/faces/{gallery_id}/{n}.jpg          # enrolled
```

## 4. APIs (additive)

Existing ingest stays. Add:

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/ingest/frame` | already ANPR; also run `analyse()` when `engines` form field set |
| POST | `/api/ingest/analyse` | multipart still; returns all events (plates, objects, faces, intrusion) |
| POST | `/api/ingest/confirm-face` | `{camera_id, gallery_id}` operator override, confidence 1.0, audited |
| GET | `/api/detections?entity_type=` | filter |
| GET | `/api/objects/report.csv` | timestamped object rows (eval 05) |
| GET | `/api/faces/gallery` | enrolled ids only, no raw embeddings in JSON |
| POST | `/api/faces/enroll` | multipart images + `gallery_id` + `name`; `Own` cameras / superadmin only |
| GET | `/api/intrusion` | open intrusion alerts |

`POST /api/ingest/confirm` (plate) is unchanged.

## 5. Matcher rules

```
on_detection(event):
  if event.plate:     hit = watchlist by plate
  elif event.face_id: hit = watchlist by gallery_id
  elif event.entity_type == 'intrusion': hit = synthetic category INTRUSION / CRITICAL
  else: no watchlist alert (object counts still stored as detections)
```

Dedupe key: `(entity_type, entity_id or plate or face_id, camera_id)` within 120 s.

## 6. UI

Keep the seven tabs. Extend:

- **Onboard:** “Analyse this still” next to “ANPR this still”. Show plate + object list + face match.
- **Watchlist:** show `entity_type` and `name`; enroll-face control for person rows.
- **Analytics & Gaps:** counts by entity_type; intrusion table; download object CSV.
- **Alerts:** person hits use name, not an empty plate.

Do not add an eighth tab unless C07 overruns; prefer extending Analytics & Gaps.

## 7. Honesty

| Situation | What the UI and CSV must say |
|---|---|
| Tesseract produced the plate | `source=anpr`, confidence from OCR |
| Operator confirm | `source=operator_confirm`, confidence 1.0 |
| Object DNN hit | `source=objects`, class + confidence |
| LBPH face match | `source=faces`, gallery_id + confidence |
| Face on a gov camera | engine skipped; test asserts zero face events |

## 8. Weights and fixtures

- Object model: vendored under `02_Code/prahari/app/models_data/` **or** downloaded once by a script into that folder and gitignored if large. Tests skip with an explicit message if weights missing **and** still pass a Haar/HOG or synthetic-blob fallback that detects a drawn rectangle labelled as `person` in a fixture PNG.
- Face fixtures: generated geometric “faces” (two eyes + mouth on a skin-tone ellipse) with unique textures per gallery id, so tests do not need real biometric data.
- Human demo: two consented adult photos. Never a minor. Never a scraped web face.

## 9. What production swap looks like (HLD text, not PoC)

- ANPR: YOLO plate + PaddleOCR behind `recognize()`.
- Objects: YOLO11 regional GPU, 1 fps.
- FRS: lawful watchlist cameras only, dedicated enrollment, human confirm, no general public matching.
- Fingerprints: AFIS/NAFIS stay outside this plane (Phase-2 API, not pixels).
