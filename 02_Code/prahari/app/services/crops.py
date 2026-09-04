"""Honest crop persistence. Matcher always sees original pixels."""

from __future__ import annotations

from typing import Any

import cv2
import numpy as np

from app import config


def fft_quality(crop_bgr: np.ndarray) -> float:
    if crop_bgr is None or getattr(crop_bgr, "size", 0) == 0:
        return 1.0
    gray = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2GRAY) if crop_bgr.ndim == 3 else crop_bgr
    if gray.size < 16:
        return 1.0
    shifted = np.fft.fftshift(np.fft.fft2(gray))
    mag = np.log(np.abs(shifted) + 1.0)
    h, w = mag.shape
    cy, cx = h // 2, w // 2
    radius = max(1, min(h, w) // 8)
    high = mag.copy()
    y0, y1 = max(0, cy - radius), min(h, cy + radius)
    x0, x1 = max(0, cx - radius), min(w, cx + radius)
    high[y0:y1, x0:x1] = 0
    return float(high.mean() / (mag.mean() + 1e-6))


def persist(
    camera_id: str,
    event_id: str,
    crop_bgr: np.ndarray | None,
    entity_type: str = "vehicle",
) -> dict[str, Any]:
    folder = config.crop_dir() / camera_id
    folder.mkdir(parents=True, exist_ok=True)
    dest = folder / f"{event_id}.jpg"
    if crop_bgr is not None:
        cv2.imwrite(str(dest), crop_bgr)
    rel = f"/crops/{camera_id}/{event_id}.jpg"
    method = "none"
    enhanced_rel = ""
    reconstructed = 0
    if crop_bgr is not None and fft_quality(crop_bgr) < 0.3:
        up = cv2.resize(crop_bgr, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        extra = folder / f"{event_id}_enhanced.jpg"
        cv2.imwrite(str(extra), up)
        enhanced_rel = f"/crops/{camera_id}/{event_id}_enhanced.jpg"
        method = "cubic_upscale"
        if (entity_type or "").lower() == "person":
            reconstructed = 1
    return {
        "crop_uri": rel,
        "crop_uri_original": rel,
        "crop_uri_enhanced": enhanced_rel,
        "enhancement_method": method,
        "is_ai_reconstructed": reconstructed,
    }
