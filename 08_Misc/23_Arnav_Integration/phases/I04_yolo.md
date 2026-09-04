# I04 — YOLO objects and plate crop

Prepend `00_MASTER_CONTEXT.md`. AGENT. Depends on I01.

## Goal

`OBJECT_ENGINE=yolo` and `ANPR_ENGINE=yolo` use Arnav’s vehicle/plate detectors when ultralytics+weights load. Defaults unchanged.

## Agent

1. Wire `objects.detect`: yolo backend classes mapped to our CLASSES set; person included (his yolo_engine currently filters vehicles only — **add class 0 person** when used as OBJECT_ENGINE).
2. Wire `anpr.recognize`: if yolo, copy the vehicle-crop-then-Tesseract logic from his `YoloEngine`. On failure, `_tesseract_recognize` full frame. Catch missing binary as we already do.
3. Weights: env `YOLO_VEHICLE_WEIGHTS` default `app/models_data/yolov8n.pt`. Script `scripts/fetch_yolo_weights.py` downloads if missing. Gitignore `*.pt` under `app/models_data/` unless the team wants the 6.5 MB file committed.
4. Tests T-V02 fallback; T-V05 skip without weights.

## Done when

- Default pytest green without ultralytics.
- CSV I04-* DONE.

## Do not

Make yolo the default. Require GPU.
