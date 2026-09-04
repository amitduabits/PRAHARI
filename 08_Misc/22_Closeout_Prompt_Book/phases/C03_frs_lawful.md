# C03 — Lawful FRS gallery (own-feed only)

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on C01. Read FRS law in the master context.

## Goal

Enrolled-gallery face match works on `CAM-OWN-001`. It is impossible to emit a face event for `cam04` or any Gov camera.

## Agent

1. `app/services/faces.py`:

```
def enroll(gallery_id: str, images_bgr: list) -> dict
def match(frame_bgr, gallery: dict | None = None) -> list[dict]
def reset(camera_id: str) -> None
```

   Detector: OpenCV Haar `haarcascade_frontalface_default.xml` (bundled with opencv) or YuNet if the `.onnx` is present. Embedder: OpenCV LBPH `cv2.face.LBPHFaceRecognizer_create` if `cv2.face` exists; else a histogram of the aligned 64×64 crop (L2 distance). Threshold in env `FACE_MATCH_MIN_CONFIDENCE` default 0.55 (convert LBPH distance to a 0–1 score; document the formula in a comment).

2. Synthetic fixtures, **not real people**:
   - `tests/fixtures/faces/WL-004/a.png` and `b.png`: 128×128 ellipse, two eye dots, unique noise seed 4.
   - `tests/fixtures/faces/WL-X/a.png`: different seed.
   - Script `scripts/make_face_fixtures.py` generates them.

3. On boot, if `data/faces/WL-004/` empty, copy synthetic fixtures so matcher tests do not need a human photo.

4. APIs:
   - `POST /api/faces/enroll` multipart, fields `gallery_id`, `name`. superadmin or soc_operator only. Writes crops under `data/faces/{gallery_id}/`. Updates watchlist gallery_id. Audit.
   - `POST /api/ingest/confirm-face` JSON `{camera_id, gallery_id}`. Camera must be ownership=Own. confidence 1.0, source=operator_confirm, entity_type=person. Audit.
   - `GET /api/faces/gallery` list of `{gallery_id, name, n_images}`. No embeddings.

5. `engines_for` already drops faces for Gov. **Additionally** inside `match` / analyse: if `re.match(r'^cam\d+', camera_id)` or ownership != Own: return [] and log `frs_refused`.

6. Tests `tests/test_faces.py` covering T-F01..T-F08. T-F04 must POST analyse to camera_id cam04 with a face-like image and assert zero events with entity_type=person.

7. HUMAN note at the end: Aria/Lead drop two consented adult photos into `03_Data/samples/faces/WL-004/` for the own-feed video. Tests must not depend on those photos.

## Done when

- test_faces.py green.
- confirm-face on CAM-OWN-001 creates an alert for WL-004.
- analyse on cam04 never creates face events.
- CSV C03-001..004 DONE. C03-005 stays HUMAN.

## Do not

Download celebrity faces. Enroll from Paldi Circle. Claim AFIS/NAFIS. Make FRS the government-feed demo. Use images of minors.
