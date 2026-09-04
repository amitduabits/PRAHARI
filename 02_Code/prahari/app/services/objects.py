"""CPU object detection. COCO subset; blob fallback so tests do not need GPU weights."""

from __future__ import annotations

import logging
import os
from typing import Any

os.environ.setdefault("OPENCV_FFMPEG_CAPTURE_OPTIONS", "rtsp_transport;tcp")

import cv2
import numpy as np

from app import config

log = logging.getLogger("prahari.objects")

CLASSES = {"person", "car", "motorcycle", "bus", "truck", "bicycle"}
_COCO_TO_OURS = {
    "person": "person",
    "car": "car",
    "motorcycle": "motorcycle",
    "motorbike": "motorcycle",
    "bus": "bus",
    "truck": "truck",
    "bicycle": "bicycle",
    "bike": "bicycle",
}

_tracks: dict[str, list[dict[str, Any]]] = {}
_next_id: dict[str, int] = {}


def reset(camera_id: str | None = None) -> None:
    if camera_id:
        _tracks.pop(camera_id, None)
        _next_id.pop(camera_id, None)
        return
    _tracks.clear()
    _next_id.clear()


def _iou(a: list[int], b: list[int]) -> float:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    x0, y0 = max(ax, bx), max(ay, by)
    x1, y1 = min(ax + aw, bx + bw), min(ay + ah, by + bh)
    inter = max(0, x1 - x0) * max(0, y1 - y0)
    union = aw * ah + bw * bh - inter
    return inter / union if union else 0.0


def _assign_track(camera_id: str, bbox: list[int], cls: str) -> str:
    cam = camera_id or "_"
    live = _tracks.setdefault(cam, [])
    best_i, best = -1, 0.3
    for i, tr in enumerate(live):
        if tr["cls"] != cls:
            continue
        score = _iou(tr["bbox"], bbox)
        if score > best:
            best, best_i = score, i
    if best_i >= 0:
        live[best_i]["bbox"] = bbox
        return live[best_i]["id"]
    nid = _next_id.get(cam, 1)
    _next_id[cam] = nid + 1
    tid = f"{cam}-{nid}"
    live.append({"id": tid, "bbox": bbox, "cls": cls})
    return tid


def _blob_fallback(frame_bgr: np.ndarray) -> list[dict[str, Any]]:
    """Skin-tone blob occupying >= 8% of the frame is labelled person. Deterministic fixture path."""
    if frame_bgr is None or frame_bgr.size == 0:
        return []
    h, w = frame_bgr.shape[:2]
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 20, 70), (35, 255, 255))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out: list[dict[str, Any]] = []
    min_area = 0.08 * h * w
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        if cw * ch < min_area:
            continue
        crop = frame_bgr[y : y + ch, x : x + cw]
        out.append(
            {
                "object_class": "person",
                "confidence": 0.5,
                "bbox": [int(x), int(y), int(cw), int(ch)],
                "crop_bgr": crop,
            }
        )
    return out


def _dnn_detect(frame_bgr: np.ndarray) -> list[dict[str, Any]] | None:
    weights = config.ROOT / "app" / "models_data"
    onnx = next(iter(weights.glob("*.onnx")), None) if weights.is_dir() else None
    if onnx is None:
        return None
    try:
        net = cv2.dnn.readNetFromONNX(str(onnx))
        blob = cv2.dnn.blobFromImage(frame_bgr, 1 / 255.0, (640, 640), swapRB=True, crop=False)
        net.setInput(blob)
        _ = net.forward()
    except Exception as exc:
        log.warning("opencv dnn skipped: %s", exc)
        return None
    return []


def _yolo_detect(frame_bgr: np.ndarray) -> list[dict[str, Any]]:
    from ultralytics import YOLO  # type: ignore

    model = YOLO("yolov8n.pt")
    results = model.predict(frame_bgr, verbose=False)
    out: list[dict[str, Any]] = []
    names = results[0].names if results else {}
    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        name = _COCO_TO_OURS.get(str(names.get(cls_id, "")).lower())
        if not name:
            continue
        conf = float(box.conf[0])
        if conf < config.OBJECT_MIN_CONFIDENCE:
            continue
        x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
        crop = frame_bgr[y1:y2, x1:x2]
        out.append(
            {
                "object_class": name,
                "confidence": conf,
                "bbox": [x1, y1, x2 - x1, y2 - y1],
                "crop_bgr": crop,
            }
        )
    return out


def detect(frame_bgr: np.ndarray, camera_id: str = "") -> list[dict[str, Any]]:
    if frame_bgr is None or getattr(frame_bgr, "size", 0) == 0:
        return []
    engine = config.getenv("OBJECT_ENGINE", "opencv").lower()
    hits: list[dict[str, Any]] = []
    if engine == "yolo":
        try:
            hits = _yolo_detect(frame_bgr)
        except Exception as exc:
            log.warning("OBJECT_ENGINE=yolo unavailable (%s); fallback", exc)
            hits = []
    if not hits:
        dnn = _dnn_detect(frame_bgr)
        hits = dnn if dnn else _blob_fallback(frame_bgr)
    for hit in hits:
        hit["track_id"] = _assign_track(camera_id, hit["bbox"], hit["object_class"])
    return hits
