# I12 demo notes — FaceNet optional, government feed still no FRS

**When.** 04 September 2026  
**FACE_ENGINE at record time.** `histogram` (default). FaceNet was **not** installed on this laptop.

## Own-feed FaceNet still — SKIPPED

Reason: `requirements-vision.txt` (torch / facenet-pytorch) is optional. Installing it is a demo-laptop step, not a CI step. Do not delay C13 YouTube for a FaceNet reshoot. Histogram FRS on Own cameras (`CAM-OWN-001`) and operator confirm-face remain the demo beat.

If a later machine has torch:

1. `pip install -r requirements-vision.txt`
2. `FACE_ENGINE=facenet` in `.env`
3. Enroll two consented adult photos into WL-004 (never a minor, never a Sentinel crop)
4. Analyse an Own still. Government cameras still refuse faces.

## Government video — no FRS

Unchanged. `engines_for()` drops `faces` for `ownership=Gov` and `cam\d+`. FaceAnalyzer is not constructed on those cameras even if `FACE_ENGINE=facenet`. Spoken gov-feed script must not show FRS. Paldi Circle (`cam04`) stays plates / tiles / confirm only.

## Human remaining (C13, not this book)

Own-feed Unlisted YouTube ≤ 3 min. Gov-feed Unlisted YouTube ≤ 3 min with no FRS. Drive Anyone+Viewer for the plate CSV. Portal receipt.
