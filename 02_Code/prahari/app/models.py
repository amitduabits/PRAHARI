"""Row helpers. Detection field names are frozen by the master context."""

from __future__ import annotations

from typing import Any


CAMERA_COLUMNS = (
    "camera_id",
    "department",
    "ownership",
    "consent",
    "lat",
    "lon",
    "protocol",
    "url",
    "retention_days",
    "cam_type",
    "health",
    "location",
    "codec",
    "width",
    "height",
    "rtsp",
    "whep",
    "hls",
    "extra_json",
)

DETECTION_COLUMNS = (
    "event_id",
    "plate",
    "plate_raw",
    "confidence",
    "camera_id",
    "lat",
    "lon",
    "ts",
    "pts_ms",
    "crop_uri",
    "category",
    "priority",
    "source_case_id",
    "entity_type",
    "entity_id",
    "face_id",
    "object_class",
    "bbox_json",
    "track_id",
    "source",
)


def row_to_dict(row: Any) -> dict[str, Any]:
    if row is None:
        return {}
    return {k: row[k] for k in row.keys()}
