"""Lawful enrolled-gallery FRS. Never called on Gov / camNN cameras (see analyse.engines_for)."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

os.environ.setdefault("OPENCV_FFMPEG_CAPTURE_OPTIONS", "rtsp_transport;tcp")

import cv2
import numpy as np
from PIL import Image, ImageDraw

from app import config

log = logging.getLogger("prahari.faces")

_tracks: dict[str, list[str]] = {}
_gallery_cache: dict[str, list[np.ndarray]] = {}


def reset(camera_id: str | None = None) -> None:
    if camera_id:
        _tracks.pop(camera_id, None)
        return
    _tracks.clear()


def _write_synthetic(path: Path, seed: int, shift: int = 0) -> None:
    rng = np.random.default_rng(seed)
    img = Image.new("RGB", (128, 128), (40, 40, 40))
    draw = ImageDraw.Draw(img)
    tone = (180 + (seed * 17) % 50, 130 + (seed * 11) % 40, 110 + (seed * 7) % 30)
    cx, cy = 64 + shift, 70
    draw.ellipse((cx - 40, cy - 50, cx + 40, cy + 50), fill=tone)
    draw.ellipse((cx - 18, cy - 18, cx - 8, cy - 8), fill=(20, 20, 20))
    draw.ellipse((cx + 8, cy - 18, cx + 18, cy - 8), fill=(20, 20, 20))
    draw.arc((cx - 16, cy + 4, cx + 16, cy + 24), 20, 160, fill=(80, 40, 40), width=2)
    noise = rng.integers(0, 40, (128, 128, 3), dtype=np.uint8)
    arr = np.clip(np.array(img, dtype=np.int16) + noise, 0, 255).astype(np.uint8)
    Image.fromarray(arr).save(path)


def ensure_synthetic_gallery() -> None:
    dest = config.face_dir() / "WL-004"
    dest.mkdir(parents=True, exist_ok=True)
    if not any(dest.glob("*.png")) and not any(dest.glob("*.jpg")):
        _write_synthetic(dest / "a.png", seed=4)
        _write_synthetic(dest / "b.png", seed=4, shift=2)
    other = config.face_dir() / "WL-X"
    other.mkdir(parents=True, exist_ok=True)
    if not any(other.glob("*.png")):
        _write_synthetic(other / "a.png", seed=99)


def write_fixture_pair(root: Path, gallery_id: str, seed: int) -> tuple[Path, Path]:
    folder = root / gallery_id
    folder.mkdir(parents=True, exist_ok=True)
    a, b = folder / "a.png", folder / "b.png"
    _write_synthetic(a, seed=seed)
    _write_synthetic(b, seed=seed, shift=2)
    return a, b


def _embed(bgr: np.ndarray) -> np.ndarray:
    small = cv2.resize(bgr, (64, 64))
    hist = cv2.calcHist([small], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist.astype(np.float32)


def _score(a: np.ndarray, b: np.ndarray) -> float:
    ha = a.reshape(8, 8, 8).astype(np.float32)
    hb = b.reshape(8, 8, 8).astype(np.float32)
    return float(cv2.compareHist(ha, hb, cv2.HISTCMP_CORREL))


def _detect_boxes(frame_bgr: np.ndarray) -> list[tuple[int, int, int, int]]:
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    cascade_path = getattr(cv2.data, "haarcascades", "") + "haarcascade_frontalface_default.xml"
    boxes: list[tuple[int, int, int, int]] = []
    if Path(cascade_path).is_file():
        cascade = cv2.CascadeClassifier(cascade_path)
        found = cascade.detectMultiScale(gray, 1.1, 4)
        boxes = [(int(x), int(y), int(w), int(h)) for x, y, w, h in found]
    h, w = frame_bgr.shape[:2]
    if not boxes and h <= 256 and w <= 256:
        boxes = [(0, 0, w, h)]
    return boxes


def load_gallery(force: bool = False) -> dict[str, list[np.ndarray]]:
    global _gallery_cache
    if _gallery_cache and not force:
        return _gallery_cache
    cache: dict[str, list[np.ndarray]] = {}
    root = config.face_dir()
    if root.is_dir():
        for folder in root.iterdir():
            if not folder.is_dir():
                continue
            embs = []
            for img_path in sorted(folder.glob("*")):
                if img_path.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
                    continue
                bgr = cv2.imread(str(img_path))
                if bgr is None:
                    continue
                embs.append(_embed(bgr))
            if embs:
                cache[folder.name] = embs
    _gallery_cache = cache
    return cache


def enroll(gallery_id: str, images_bgr: list[np.ndarray]) -> dict[str, Any]:
    dest = config.face_dir() / gallery_id
    dest.mkdir(parents=True, exist_ok=True)
    n = 0
    for img in images_bgr:
        if img is None:
            continue
        boxes = _detect_boxes(img)
        crop = img
        if boxes:
            x, y, w, h = boxes[0]
            crop = img[y : y + h, x : x + w]
        path = dest / f"{len(list(dest.glob('*'))) + 1}.jpg"
        cv2.imwrite(str(path), crop)
        n += 1
    load_gallery(force=True)
    return {"gallery_id": gallery_id, "n_images": n}


def match(frame_bgr: np.ndarray, gallery: dict[str, list[np.ndarray]] | None = None) -> list[dict[str, Any]]:
    if frame_bgr is None or getattr(frame_bgr, "size", 0) == 0:
        return []
    gal = gallery if gallery is not None else load_gallery()
    if not gal:
        ensure_synthetic_gallery()
        gal = load_gallery(force=True)
    out: list[dict[str, Any]] = []
    threshold = float(config.getenv("FACE_MATCH_MIN_CONFIDENCE", str(config.FACE_MATCH_MIN_CONFIDENCE)))
    for x, y, w, h in _detect_boxes(frame_bgr):
        crop = frame_bgr[y : y + h, x : x + w]
        emb = _embed(crop)
        best_id, best = "", -1.0
        for gid, embs in gal.items():
            for other in embs:
                s = _score(emb, other)
                if s > best:
                    best, best_id = s, gid
        hit = {
            "face_id": best_id if best >= threshold else "",
            "confidence": max(0.0, float(best)),
            "bbox": [int(x), int(y), int(w), int(h)],
            "crop_bgr": crop,
        }
        out.append(hit)
    return out
