"""Lazy FaceNet backend. Torch is imported only inside FaceAnalyzer.__init__."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

log = logging.getLogger("prahari.facenet")

_analyzer: Any = None


class FaceAnalyzer:
    """MTCNN boxes + InceptionResnetV1 512-d embeddings. Constructed only on Own cameras."""

    def __init__(self) -> None:
        import torch
        from facenet_pytorch import MTCNN, InceptionResnetV1

        self._torch = torch
        self.mtcnn = MTCNN(keep_all=True, device="cpu")
        self.resnet = InceptionResnetV1(pretrained="vggface2").eval().to("cpu")

    def extract_faces(self, frame_bgr: np.ndarray) -> list[dict[str, Any]]:
        if frame_bgr is None or getattr(frame_bgr, "size", 0) == 0:
            return []
        import cv2

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        boxes, probs = self.mtcnn.detect(frame_rgb)
        results: list[dict[str, Any]] = []
        if boxes is None:
            return results
        torch = self._torch
        for bbox, prob in zip(boxes, probs):
            if prob is None or bbox is None:
                continue
            x1, y1, x2, y2 = [int(b) for b in bbox]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(frame_bgr.shape[1], x2), min(frame_bgr.shape[0], y2)
            if x2 <= x1 or y2 <= y1:
                continue
            crop_rgb = frame_rgb[y1:y2, x1:x2].copy()
            crop_resized = cv2.resize(crop_rgb, (160, 160))
            crop_tensor = torch.tensor(crop_resized).permute(2, 0, 1).float()
            crop_tensor = (crop_tensor - 127.5) / 128.0
            crop_tensor = crop_tensor.unsqueeze(0)
            with torch.no_grad():
                embedding = self.resnet(crop_tensor).squeeze(0).detach().cpu().numpy().astype(np.float32)
            results.append(
                {
                    "bbox": [x1, y1, x2 - x1, y2 - y1],
                    "confidence": float(prob),
                    "crop": frame_bgr[y1:y2, x1:x2].copy(),
                    "embedding": embedding,
                }
            )
        return results


def get_analyzer() -> FaceAnalyzer:
    """Lazy singleton. Call only after engines_for() has allowed faces."""
    global _analyzer
    if _analyzer is None:
        _analyzer = FaceAnalyzer()
    return _analyzer


def reset_analyzer() -> None:
    global _analyzer
    _analyzer = None


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    va = np.asarray(a, dtype=np.float32).flatten()
    vb = np.asarray(b, dtype=np.float32).flatten()
    na, nb = float(np.linalg.norm(va)), float(np.linalg.norm(vb))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return float(np.dot(va, vb) / (na * nb))
