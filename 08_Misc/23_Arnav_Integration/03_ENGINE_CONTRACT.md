# Engine contract after Arnav integration

`analyse()` remains the only worker. Arnav’s modules are backends.

## 1. Env (add to `.env.example`, not required in `.env`)

```
ANPR_ENGINE=tesseract          # or yolo
OBJECT_ENGINE=opencv           # or yolo
FACE_ENGINE=histogram          # or facenet
TRACK_ENGINE=iou               # or bytetrack
ANALYTICS_ENGINES=anpr,objects # faces added only for Own cameras
```

`requirements.txt` stays the C12 set (FastAPI, OpenCV, Tesseract, pytest). New file `requirements-vision.txt`:

```
torch
torchvision
facenet-pytorch
ultralytics>=8.0.0
lapx>=0.5.5
```

Do not add insightface/onnxruntime until AdaFace weights exist.

## 2. faces.py

```
def match(frame_bgr, gallery=None) -> list[dict]:
    engine = getenv FACE_ENGINE
    if engine == facenet:
        try: return facenet_match(...)
        except ImportError: fall through
    return histogram_match(...)   # current C03 path
```

Facenet path: MTCNN boxes + 512-d embedding; cosine against enrolled gallery embeddings stored as `.npy` next to `data/faces/{gallery_id}/`. Gallery JSON still has no embedding bytes.

`engines_for()` still drops `faces` for Gov and `cam\d+` **before** `match()` is called. Facenet must not be constructed for those cameras (lazy init inside the Own branch only).

## 3. objects.py / anpr.py

`detect()`: if `OBJECT_ENGINE=yolo` and ultralytics+weights load, use COCO subset; else blob fallback.

`recognize()`: if `ANPR_ENGINE=yolo`, vehicle crop then plate then Tesseract; on any failure, morphology+Tesseract on the full frame (current path).

## 4. Track ids

`objects.detect` assigns `track_id`. If `TRACK_ENGINE=bytetrack` and import works, ByteTrack; else IoU. `capture` scene-cut still calls `objects.reset` and `faces.reset`.

## 5. Crops

Always write `crop_uri_original`. Optional `crop_uri_enhanced` for human review. Auto-match uses **original** pixels only. If `is_ai_reconstructed` is true, matcher must not fire a CRITICAL from that crop; alert status `pending_review`.

## 6. APIs (additive)

| Path | Role |
|---|---|
| existing ingest/analyse, confirm, confirm-face, faces/enroll | unchanged contracts |
| GET `/api/predict/{plate}` | next cameras, historical then GIS |
| POST `/api/query` | optional; response must include `engine: "keyword_rules"` |
| GET `/api/faces/gallery` | still no embeddings |

## 7. UI

Keep seven tabs. Watchlist: his person-enroll form posting `/api/faces/enroll`. Track tab: optional “Next cameras” calling `/api/predict/GJ01AB1234`. Alerts: show `pending_review`. Onboard Analyse still already exists.

## 8. Docs honesty

HLD §6: histogram FRS and blob objects are the no-GPU PoC. FaceNet and YOLO are optional engines when `requirements-vision.txt` is installed. CodeFormer/ESRGAN/AdaFace are **not** in this PoC.

Slides: one frame “Optional vision engines (Arnav)”. One bullet FRS law. 80k still DESIGN TARGET.
