"""recognize() is the only AI interface. Tesseract now; YOLO later behind ANPR_ENGINE."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

from app import config
from app.services.plates import normalise

log = logging.getLogger("prahari.anpr")


def _tesseract_recognize(frame_bgr: np.ndarray) -> dict[str, Any]:
    import cv2
    import pytesseract

    try:
        pytesseract.get_tesseract_version()
    except Exception:
        return {"plate": None, "plate_raw": "", "confidence": 0.0, "crop_bgr": frame_bgr, "box": None}

    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 5))
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    _, thresh = cv2.threshold(blackhat, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    h, w = gray.shape[:2]
    box = None
    crop = frame_bgr
    best = None
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        if ch == 0:
            continue
        aspect = cw / ch
        if 2.0 <= aspect <= 6.5 and cw > w * 0.15:
            best = (x, y, cw, ch)
            break
    if best:
        x, y, cw, ch = best
        pad = 4
        x0, y0 = max(0, x - pad), max(0, y - pad)
        crop = frame_bgr[y0 : y + ch + pad, x0 : x + cw + pad]
        box = [int(x0), int(y0), int(cw), int(ch)]
    rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    config_str = "--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    text = pytesseract.image_to_string(rgb, config=config_str)
    plate_raw = "".join(ch for ch in text if ch.isalnum() or ch in " -")
    plate = normalise(plate_raw)
    data = pytesseract.image_to_data(rgb, config=config_str, output_type=pytesseract.Output.DICT)
    confs = [int(c) for c in data.get("conf", []) if str(c).lstrip("-").isdigit() and int(c) >= 0]
    mean = (sum(confs) / len(confs) / 100.0) if confs else (0.5 if plate else 0.0)
    if plate and mean <= 0:
        mean = 0.5
    if not plate or mean < config.ANPR_MIN_CONFIDENCE:
        return {"plate": None, "plate_raw": plate_raw.strip(), "confidence": mean, "crop_bgr": crop, "box": box}
    return {"plate": plate, "plate_raw": plate_raw.strip(), "confidence": mean, "crop_bgr": crop, "box": box}


def _crop_xyxy(frame_bgr: np.ndarray, box: list[float]) -> tuple[np.ndarray, list[int]]:
    x1, y1, x2, y2 = [int(v) for v in box[:4]]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(frame_bgr.shape[1], x2), min(frame_bgr.shape[0], y2)
    if x2 <= x1 or y2 <= y1:
        return frame_bgr, [0, 0, int(frame_bgr.shape[1]), int(frame_bgr.shape[0])]
    return frame_bgr[y1:y2, x1:x2], [x1, y1, x2 - x1, y2 - y1]


class YoloEngine:
    def recognize(self, frame_bgr: np.ndarray) -> dict[str, Any]:
        from app.engines.yolo_backend import detect_plate, detect_vehicles

        vehicles = detect_vehicles(frame_bgr)
        if not vehicles:
            return _tesseract_recognize(frame_bgr)
        vehicle_crop, vehicle_box = _crop_xyxy(frame_bgr, vehicles[0].box)
        plate = detect_plate(vehicle_crop)
        crop = vehicle_crop
        box = vehicle_box
        if plate is not None and plate.box:
            crop, local = _crop_xyxy(vehicle_crop, plate.box)
            box = [vehicle_box[0] + local[0], vehicle_box[1] + local[1], local[2], local[3]]
        result = _tesseract_recognize(crop)
        if result.get("plate"):
            result["box"] = box
            result["crop_bgr"] = crop
            return result
        return _tesseract_recognize(frame_bgr)


def recognize(frame_bgr: np.ndarray) -> dict[str, Any]:
    engine = config.getenv("ANPR_ENGINE", "tesseract").lower()
    if engine == "yolo":
        try:
            return YoloEngine().recognize(frame_bgr)
        except Exception as exc:
            log.warning("ANPR_ENGINE=yolo unavailable (%s); tesseract fallback", exc)
    return _tesseract_recognize(frame_bgr)
