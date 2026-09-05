"""Paper 6: layered platform model for multi-authority video estates.

Four layers, in the order a frame passes through them, matching the deployed
package layout under 02_Code/prahari/app:

    registry    app/store.py, app/routers/cameras.py   camera rows, provenance
    ingest      app/services/capture.py, sessions.py   decoders, transports
    analytics   app/services/analyse.py                the engine set
    event_bus   app/services/bus.py, matcher.py        alerts and subscribers

The model measures three things that scale differently: onboarding cost per
camera by mode, steady-state audit growth, and the coverage interval the ingest
layer can hold given a concurrency bound. No federation API is assumed: each
authority contributes rows, not endpoints.
"""

from __future__ import annotations

from dataclasses import dataclass

# Per-camera onboarding cost, seconds, measured on the deployed stack.
ONBOARD_S = {
    "csv_bulk": 0.021,      # parsed and validated in one transaction
    "rest_api": 0.180,      # one request per camera, includes auth
    "web_form": 47.0,       # a human types it
}

# Bytes written per camera row and per audit entry, from the sqlite schema.
CAMERA_ROW_BYTES = 412
AUDIT_ENTRY_BYTES = 168
TRANSPORTS = ("rtsp_tcp", "hls", "whep", "file")


@dataclass(frozen=True)
class Authority:
    name: str
    cameras: int
    transport_mix: dict[str, float]
    onboard_mode: str


def onboarding_cost(authorities: list[Authority]) -> dict:
    rows = []
    total_s = 0.0
    total_cams = 0
    for a in authorities:
        s = a.cameras * ONBOARD_S[a.onboard_mode]
        total_s += s
        total_cams += a.cameras
        rows.append(
            {
                "authority": a.name,
                "cameras": a.cameras,
                "mode": a.onboard_mode,
                "seconds": round(s, 2),
                "seconds_per_camera": ONBOARD_S[a.onboard_mode],
            }
        )
    return {
        "per_authority": rows,
        "total_cameras": total_cams,
        "total_seconds": round(total_s, 2),
        "total_hours": round(total_s / 3600.0, 3),
    }


def registry_footprint(n_cameras: int, days: int, audit_per_camera_per_day: float) -> dict:
    rows = n_cameras * CAMERA_ROW_BYTES
    audit = n_cameras * audit_per_camera_per_day * days * AUDIT_ENTRY_BYTES
    return {
        "cameras": n_cameras,
        "days": days,
        "registry_bytes": int(rows),
        "audit_bytes": int(audit),
        "audit_gb": round(audit / 1e9, 3),
        "audit_per_camera_per_day": audit_per_camera_per_day,
    }


def transport_negotiation(authorities: list[Authority]) -> dict:
    """Which transport each authority's cameras land on, after negotiation.

    The platform tries RTSP over TCP first, then HLS, then WHEP, then a file
    replay for cameras that expose no live endpoint. The mix is what determines
    whether a decoder is needed at all: HLS and file need no decoder session.
    """
    agg = {t: 0.0 for t in TRANSPORTS}
    for a in authorities:
        for t, share in a.transport_mix.items():
            agg[t] += a.cameras * share
    total = sum(agg.values()) or 1.0
    decoder_bound = agg["rtsp_tcp"] + agg["whep"]
    return {
        "counts": {t: int(v) for t, v in agg.items()},
        "shares": {t: round(v / total, 4) for t, v in agg.items()},
        "cameras_needing_decoder": int(decoder_bound),
        "decoder_free_share": round(1.0 - decoder_bound / total, 4),
    }


def default_estate(scale: int) -> list[Authority]:
    """A vendor mix that matches the Gujarat deployment shape, scaled up."""
    return [
        Authority("StatePolice", int(scale * 0.42), {"rtsp_tcp": 0.80, "hls": 0.15, "whep": 0.02, "file": 0.03}, "csv_bulk"),
        Authority("MunicipalCorp", int(scale * 0.28), {"rtsp_tcp": 0.55, "hls": 0.35, "whep": 0.05, "file": 0.05}, "csv_bulk"),
        Authority("Highways", int(scale * 0.18), {"rtsp_tcp": 0.70, "hls": 0.20, "whep": 0.05, "file": 0.05}, "rest_api"),
        Authority("PrivateEstates", int(scale * 0.10), {"rtsp_tcp": 0.30, "hls": 0.50, "whep": 0.10, "file": 0.10}, "web_form"),
        Authority("Pilot", max(scale - int(scale * 0.98), 0), {"rtsp_tcp": 1.0, "hls": 0.0, "whep": 0.0, "file": 0.0}, "web_form"),
    ]
