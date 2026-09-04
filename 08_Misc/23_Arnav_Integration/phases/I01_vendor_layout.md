# I01 — Vendor layout

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on I00.

## Goal

Arnav’s selected modules live under our tree as import-guarded engines. His repo is a read-only fetch.

## Agent

1. Clone `https://github.com/ArAv-1/PRAHARI-3.0.git` to `08_Misc/23_Arnav_Integration/_upstream/` if missing. Add `_upstream/` to `.gitignore` at repo root or this book folder.
2. Create `02_Code/prahari/app/engines/__init__.py`.
3. Copy **only**:
   - `face_rec.py` → `app/engines/facenet_backend.py` (rename class usage later in I02)
   - `yolo_engine.py` → `app/engines/yolo_backend.py`
   - `bytetrack_engine.py` → `app/engines/bytetrack_backend.py`
   - `predictive.py` logic will be rewritten in I08 against our store (do not copy the FastAPI router blindly if it is not a service).
4. Do **not** copy `ai_judge.py`, `vendor/adaface`, `enhance.py` yet (I06 will take the honest bits only).
5. Write `requirements-vision.txt` as in `03_ENGINE_CONTRACT.md`.
6. Add `FACE_ENGINE`, `OBJECT_ENGINE`, `TRACK_ENGINE` to `app/config.py` getenv helpers (defaults histogram / opencv / iou).
7. `.env.example` comments: vision extras optional.
8. README: one paragraph “Optional vision engines (torch). Default path needs no GPU.”

## Done when

- `python -c "from app.engines import yolo_backend"` does not import torch at package import if you lazy-import inside functions. Prefer lazy imports inside functions.
- pytest still green without installing vision extras.
- CSV I01-* DONE.

## Do not

Copy `yolov8n.pt` into git unless the team agrees. Copy `index.html` wholesale (would drop Analyse this still and DESIGN TARGET footer).
