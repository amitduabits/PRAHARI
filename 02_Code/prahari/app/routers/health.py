from __future__ import annotations

from fastapi import APIRouter

from app import config
from app.db import count_table

router = APIRouter()


@router.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "cameras": count_table("cameras"),
        "detections": count_table("detections"),
        "watchlist": count_table("watchlist"),
        "sentinel_host_configured": config.sentinel_host_configured(),
    }
