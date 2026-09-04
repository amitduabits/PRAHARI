# What to take from ArAv-1/PRAHARI-3.0

Read against https://github.com/ArAv-1/PRAHARI-3.0 (tree as of 03 Sep 2026). His README still describes the 31 Aug plate plane. The extra engines live under `02_Code/prahari/app/services/` and tests.

## Take (copy, then adapt to our doors)

| His file | Becomes | Why |
|---|---|---|
| `app/services/face_rec.py` | `FACE_ENGINE=facenet` inside `faces.py` or `engines/facenet.py` | Real 512-d embeddings. Our histogram stays default. |
| Person enroll form in `index.html` | Watchlist tab “Enroll person” | We have the API; his UI is the demo beat. |
| `app/services/yolo_engine.py` | `OBJECT_ENGINE=yolo` / `ANPR_ENGINE=yolo` | Vehicle box then plate crop then OCR. |
| `yolov8n.pt` | `app/models_data/yolov8n.pt` **gitignored** if >1 MB, or download script | Do not force 6.5 MB into every clone if policy forbids. Prefer download-once. |
| `bytetrack_engine.py` | `TRACK_ENGINE=bytetrack` | Eval 05 person/vehicle tracking. |
| `tracker.py` tracklet window | Optional helper `get_tracklet()` | Same-camera grouping. Not GIS reconstruction. |
| `predictive.py` | `GET /api/predict/{plate}` | Bonus next-camera. |
| Original crop fields in ingest | `crop_uri_original`, `is_ai_reconstructed` | Honesty. |
| `pending_review` alert status | Alerts tab | Human in the loop for low confidence. |
| `docs/data-retention-policy.md` | `04_Documents/` or `02_Code/prahari/docs/` after a claims pass | DPDP bonus text. Strip AdaFace/CodeFormer names unless true. |

## Adapt (the idea is good; his implementation is not shippable as labelled)

| His claim | Reality | Our label |
|---|---|---|
| CodeFormer reconstruction | `cv2.GaussianBlur` | `enhancement_method=blur_review` for human view only |
| Real-ESRGAN | `cv2.resize(..., INTER_CUBIC)` | `enhancement_method=cubic_upscale` |
| AdaFace judge | Toy `nn.Conv2d` + linear; `data/adaface_weights.pt` **missing** | Do not ship. Optional later if weights exist |
| `extract_adaface` / `enhance_codeformer` in `face_rec.py` | Return `[]` / identity | Delete or leave dead, never call from ingest |
| `/api/query` “NLP” | Colour/type regex | Ship only as “keyword filter”, not NLP |
| `test_face.py` | Wrong ctor `name=buffalo_s`; downloads Grace Hopper | Do not copy. Use synthetic or consented fixtures |

## Refuse (would destroy strengths)

| His behaviour | Why refuse |
|---|---|
| `ingest_frame` always runs `FaceAnalyzer` | FRS on Paldi Circle. Our T-F04/T-F05 fail. |
| Footer “At 80,000 cameras we sample 1 fps” without DESIGN TARGET | `audit_gate` K3 |
| README catalogue `/api/ingest` | Live host 404. We use `/cameras.json`. |
| Default `torch`, `ultralytics`, `facenet-pytorch` in requirements | Laptop demo dies if pip is slow. Keep extras in `requirements-vision.txt`. |
| Whole-repo merge / change `origin` to ArAv-1 | Wipes path jail, HMAC, vendored HLS, C00–C12 tests. |
| Wikipedia face download in tests | Unstable, not consented, not our gallery law. |

## Already stronger in ours (do not replace)

Sentinel catalogue client, HLS origin pin, path jail, HMAC tokens, vendored `hls.min.js`, `engines_for()` Gov refuse, intrusion ROI, experiment harness, SCALE_BENCH, BITS notes/slides with FRS law, 74 pytest.

## Version naming

Call this layer **PRAHARI engine pack v3** or **optional vision engines**, not a new product. Submission GitHub remains https://github.com/amitduabits/PRAHARI. Arnav’s repo may stay a public workshop. Do not ask the committee to clone ArAv-1.
