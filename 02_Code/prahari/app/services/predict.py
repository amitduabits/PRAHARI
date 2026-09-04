"""Next-camera list: historical transition frequency, else GIS neighbours. Not Kalman."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from app import store


def predict_next(plate: str) -> dict[str, Any]:
    plate = (plate or "").upper()
    dets = store.list_detections(plate=plate)
    if not dets:
        return {"predictions": [], "note": "No history found for entity.", "method": "frequency+distance"}
    last_cam_id = dets[-1].get("camera_id") or ""
    if not last_cam_id:
        return {"predictions": [], "note": "Last detection has no camera_id.", "method": "frequency+distance"}

    tracks: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in store.list_detections():
        p = (row.get("plate") or "").upper()
        if p:
            tracks[p].append(row)

    transitions: dict[str, int] = defaultdict(int)
    for _, track in tracks.items():
        if len(track) < 2:
            continue
        for i in range(len(track) - 1):
            c1 = track[i].get("camera_id")
            c2 = track[i + 1].get("camera_id")
            if c1 == last_cam_id and c1 != c2 and c2:
                transitions[str(c2)] += 1

    if transitions:
        total = sum(transitions.values()) or 1
        ranked = sorted(transitions.items(), key=lambda x: x[1], reverse=True)[:3]
        predictions = [
            {
                "camera_id": cam,
                "probability": float(count) / total,
                "note": "historical transition frequency",
            }
            for cam, count in ranked
        ]
        return {
            "predictions": predictions,
            "note": "Historical transition frequencies.",
            "method": "frequency+distance",
        }

    last_cam = store.get_camera(last_cam_id) or {}
    lat1 = float(last_cam.get("lat") or 0)
    lon1 = float(last_cam.get("lon") or 0)
    dists = []
    for cam in store.list_cameras():
        if cam["camera_id"] == last_cam_id:
            continue
        dist = store.haversine_km(lat1, lon1, float(cam.get("lat") or 0), float(cam.get("lon") or 0))
        dists.append((cam["camera_id"], dist))
    dists.sort(key=lambda x: x[1])
    predictions = [
        {
            "camera_id": cam,
            "probability": 1.0 / (i + 2),
            "note": f"geographically close ({dist:.1f} km)",
        }
        for i, (cam, dist) in enumerate(dists[:3])
    ]
    return {
        "predictions": predictions,
        "note": "Based on geographical proximity (no historical transitions).",
        "method": "frequency+distance",
    }
