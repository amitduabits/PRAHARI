# Tests for the Arnav engine pack

Old C-suite tests stay. New ids `T-V*` (vision). Skip with an explicit reason if torch/ultralytics/weights are missing. Default engines must still pass.

## Must stay green (regressions)

| ID | Assert |
|---|---|
| T-W04 | `GET /api/track/GJ01AB1234` count ≥ 6, seed order |
| T-F04 / T-F05 | analyse on `cam04` / Gov → zero `entity_type=person` even if `FACE_ENGINE=facenet` |
| T-K02 | confirm `source=operator_confirm` |
| T-K03 | footer contains DESIGN TARGET near 80,000 |
| T-S07 | `frs_refused` in `analyse.py`; FaceAnalyzer not constructed on Gov |
| integrator | TCP, no CAP_PROP_FPS, scene-cut reset |

## New

| ID | File | Assert |
|---|---|---|
| T-V01 | `test_engine_fallback.py` | `FACE_ENGINE=facenet` without torch → histogram path, no crash |
| T-V02 | `test_engine_fallback.py` | `OBJECT_ENGINE=yolo` / `ANPR_ENGINE=yolo` without ultralytics → blob / tesseract path |
| T-V03 | `test_facenet_optional.py` | if torch+facenet-pytorch: two consented or synthetic faces, same gallery cosine > other gallery |
| T-V04 | `test_privacy_frs.py` | `FACE_ENGINE=facenet` + Own-only: `cam04` still zero person events (do not even import FaceAnalyzer if engines_for dropped faces) |
| T-V05 | `test_yolo_optional.py` | if yolov8n present: person or vehicle class on a real still; else skip |
| T-V06 | `test_bytetrack_optional.py` | if ultralytics: track_id stable across two overlapping boxes; reset clears state |
| T-V07 | `test_crops_honesty.py` | original uri set; enhanced method is `none` or `cubic_upscale`/`blur_review`; reconstructed crop does not auto CRITICAL |
| T-V08 | `test_predict.py` | `GET /api/predict/GJ01AB1234` returns a list; no crash with one point |
| T-V09 | `test_query_rules.py` | if shipped: body has `engine: keyword_rules`; not `nlp` / `llm` |
| T-V10 | `test_enroll_ui.py` | GET `/` contains `Enroll` and posts still 403 for home.viewer |
| T-V11 | `test_no_forbidden_model_names.py` | grep services: no `codeformer`/`realesrgan`/`adaface` string unless a loader that checks a file path succeeded (prefer zero hits) |

## Experiments

| Exp | Pass |
|---|---|
| E-V1 | histogram FRS still matches WL-004 fixtures |
| E-V2 | FaceNet skip or MEASURED cosine on Own still |
| E-V3 | YOLO skip or MEASURED classes on own_feed frame |
| E-V4 | `cam04` + FACE_ENGINE=facenet → 0 person events MEASURED |
| E-V5 | predict GJ01AB1234 returns ≥1 camera id or honest empty |

Append to `05_Output/experiments/EXPERIMENT_LOG.md`.
