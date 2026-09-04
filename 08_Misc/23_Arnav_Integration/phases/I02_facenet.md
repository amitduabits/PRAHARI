# I02 — FACE_ENGINE=facenet

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on I01.

## Goal

Enrolled-gallery match can use FaceNet 512-d vectors when torch is installed. Histogram remains default.

## Agent

1. In `app/services/faces.py`, branch on `config.getenv("FACE_ENGINE", "histogram")`.
2. Facenet backend: lazy-import `FaceAnalyzer` from `app.engines.facenet_backend`. Detect + embed. Cosine similarity against `.npy` files under `face_dir()/gallery_id/`. Threshold env `FACE_MATCH_MIN_CONFIDENCE` (for cosine, document 0.5 as starting MEASURED later).
3. `enroll()`: if facenet loads, write embedding `.npy` next to the jpg. Histogram enroll still writes images for the default engine.
4. Fix his `FaceAnalyzer.__init__` if you keep a `name` kwarg unused. Do not download Wikipedia.
5. Tests T-V01 (no torch → no crash) in `tests/test_engine_fallback.py`. T-V03 skip unless imports work.

## Done when

- Default `FACE_ENGINE` unset: C03 histogram tests still pass.
- `FACE_ENGINE=facenet` without torch: match() still returns a list.
- CSV I02-* DONE.

## Do not

Construct FaceAnalyzer at module import. Enroll Wikipedia faces. Change Own-only policy (I03).
