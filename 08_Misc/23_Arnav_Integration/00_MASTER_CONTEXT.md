# MASTER CONTEXT — prepend to every Arnav-integration session

Copy from the line below through the end of this file into the top of every agent turn that writes or edits PRAHARI.

---

You are integrating **selected engines from Arnav’s fork** into **PRAHARI** (https://github.com/amitduabits/PRAHARI). You are not replacing the product.

## Identity

- Product: PRAHARI — statewide CCTV intelligence plane.
- Architecture: Hybrid. Model 1 registry+GIS. Model 2 unified viewing+ANPR. Thin Model 3 event bus. Model 4 Phase-2 selected cameras only.
- Team: Lead + Arnav + Aria. Arnav’s fork: https://github.com/ArAv-1/PRAHARI-3.0
- Seeded plate: `GJ01AB1234` / `WL-001` STOLEN. Do not drop the six seed points.
- Working tree: `D:\1_Projects\Research_Ongoing\PRAHARI\02_Code\prahari`
- This book: `D:\1_Projects\Research_Ongoing\PRAHARI\08_Misc\23_Arnav_Integration`
- Fetch source (read-only): clone or sparse-checkout ArAv-1/PRAHARI-3.0 into a **temp** folder, never into `02_Code/prahari`.

Application code lives only under `02_Code/prahari/`. Do not write a second app. Do not `git remote set-url` to ArAv-1.

## Integrator laws (unchanged)

1. RTSP over TCP. HLS if 8554 blocked.
2. Event time is PTS, never `CAP_PROP_FPS`, never arrival wall-clock.
3. Inter-frame gaps are not disconnects.
4. Backoff 2 s .. 30 s.
5. Decoder warnings at join are logged, not fatal.
6. Camera list from `/cameras.json`. Never invent sandbox ids.
7. Mixed H.264 / H.265.
8. Scene cut resets object and face track ids.
9. Consume only. No wget of `/stream/<id>`.
10. `MAX_OPEN_CAPTURES` default 4.

## FRS law (unchanged, Arnav’s ingest violated this)

1. Faces run only on `ownership=Own` cameras (own-feed / enrolled gallery).
2. Never detect, embed, store, or match faces from government CCTV of unknown people (`cam\d+` or `ownership=Gov`).
3. Never claim AFIS, NAFIS, or a live ministry pipe.
4. Government-feed demo: ANPR + objects only.
5. Operator confirm-face exists. Reconstructed / upscaled crops are for human review, never auto-matched.
6. Spoken: “representative person watchlist, enrolled gallery, human in the loop”.

## Engine doors (do not invent a second pipeline)

| Env | Default (keep) | Arnav swap (import-guarded) |
|---|---|---|
| `ANPR_ENGINE` | `tesseract` | `yolo` → his `yolo_engine.detect_vehicles` then plate crop then OCR |
| `OBJECT_ENGINE` | `opencv` (blob fallback) | `yolo` → COCO person/car/motorcycle/bus/truck/bicycle |
| `FACE_ENGINE` | `histogram` (current `faces.py`) | `facenet` → his `FaceAnalyzer` (MTCNN + InceptionResnetV1) |
| `TRACK_ENGINE` | IoU in `objects.py` | `bytetrack` if ultralytics imports |

If the swap import or weights fail, fall back to the default. Tests without torch/ultralytics skip the swap path and still pass the default path.

## Detection JSON

Plate fields stay frozen. Additive fields from C01 stay. New additive fields from this book:

```
crop_uri_original, crop_uri_enhanced, enhancement_method,
is_ai_reconstructed, face_vector (never in GET /api/faces/gallery),
pending_review (alert status)
```

`source` honesty: `anpr` | `operator_confirm` | `objects` | `faces` | `intrusion`. Enhancement method is `none` | `cubic_upscale` | `blur_review`. Do **not** write `codeformer`, `realesrgan`, or `adaface` unless that exact model file loaded.

## Locked content

- Hybrid model. Seeded plate. Port 8080. Integrator laws. FRS law.
- Representative watchlist language.
- `audit_gate.py` must still PASS after every phase.

## Forbidden

- Merging ArAv-1 as the new root.
- Running FaceAnalyzer on `cam04`.
- Claiming CodeFormer / Real-ESRGAN / AdaFace without weights on disk that `torch.load` succeeds.
- Dropping histogram FRS or blob objects (they are the no-GPU path).
- Kafka / K8s / Ceph.
- Rebuilding P00–P08, A00–A08, or C00–C11 unless a test is red.
- Downloading Wikipedia faces in tests.

## Definition of done

1. Files under `02_Code/prahari/` as specified.
2. `python -m pytest -q` green. New tests named in the phase exist. Old FRS-law and track tests still pass.
3. Default engines work without torch.
4. Tick `csv/integration_actions.csv`.
5. Docs match code. If FaceNet is optional, slides say optional.
