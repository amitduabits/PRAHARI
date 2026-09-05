"""FRS / faces invocation gate. Shared by analyse() and enroll."""

from __future__ import annotations

import re
from typing import Any

CAM_RE = re.compile(r"^cam\d+", re.I)

REGION_NEEDLES = (
    ("ahmedabad", ("ahmedabad", "paldi", "sg highway", "narol", "janpath", "chiman", "visat", "mall")),
    ("saurashtra", ("junagadh", "somnath", "gir", "timbavadi", "majewadi", "bypass", "char-chowk")),
    ("south", ("valsad", "surat", "adajan", "navsari")),
    ("central", ("gandhinagar", "gnr", "koba", "vadodara", "dahod", "godown", "rto")),
)


def camera_id_of(camera: dict[str, Any]) -> str:
    return str(camera.get("camera_id") or camera.get("id") or "")


def is_sandbox_id(camera_id: str) -> bool:
    return bool(CAM_RE.match(str(camera_id or "")))


def faces_allowed(camera: dict[str, Any]) -> bool:
    """True only for Own cameras that are not sandbox camNN ids."""
    ownership = str(camera.get("ownership") or "")
    return ownership == "Own" and not is_sandbox_id(camera_id_of(camera))


def refuse_reason(camera: dict[str, Any]) -> str:
    if faces_allowed(camera):
        return ""
    cam_id = camera_id_of(camera)
    ownership = str(camera.get("ownership") or "")
    if is_sandbox_id(cam_id):
        return "sandbox_id"
    if ownership != "Own":
        return "ownership_not_own"
    return "frs_refused"


def region_of(camera: dict[str, Any]) -> str:
    blob = " ".join(
        str(camera.get(k) or "") for k in ("location", "name", "department", "camera_id", "id")
    ).lower()
    for region, needles in REGION_NEEDLES:
        if any(n in blob for n in needles):
            return region
    if is_sandbox_id(camera_id_of(camera)):
        return "ahmedabad"
    return "other"


def classify_row(row: dict[str, Any]) -> dict[str, Any]:
    """Attach ownership, FRS eligibility, and region. Catalogue rows default Gov."""
    out = dict(row)
    cam_id = camera_id_of(out)
    out["camera_id"] = cam_id
    ownership = str(out.get("ownership") or "")
    if not ownership:
        ownership = "Own" if cam_id.upper().startswith("CAM-OWN") else "Gov"
    if is_sandbox_id(cam_id):
        ownership = "Gov"
    out["ownership"] = ownership
    out["frs_eligible"] = faces_allowed(out)
    out["region"] = region_of(out)
    out["sandbox"] = is_sandbox_id(cam_id)
    return out
