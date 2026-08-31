from __future__ import annotations

import asyncio

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect

from app import store
from app.auth import User, assert_write, require_user
from app.services import bus

router = APIRouter()


@router.get("/api/alerts")
def list_alerts(status: str | None = "open", user: User = Depends(require_user)) -> list[dict]:
    rows = store.list_alerts(status=status if status != "all" else None)
    if user.role == "dept_viewer":
        allowed = {c["camera_id"] for c in store.list_cameras(department=user.department)}
        rows = [r for r in rows if r.get("camera_id") in allowed]
    return rows


@router.post("/api/alerts/{alert_id}/ack")
def ack(alert_id: str, user: User = Depends(require_user)) -> dict:
    assert_write(user)
    row = store.get_alert(alert_id)
    if not row:
        raise HTTPException(status_code=404, detail="unknown alert")
    store.ack_alert(alert_id, user.username)
    store.audit(user.username, "alert_ack", alert_id)
    return store.get_alert(alert_id) or {}


@router.websocket("/ws/alerts")
async def ws_alerts(ws: WebSocket) -> None:
    await ws.accept()
    queue = bus.subscribe()
    try:
        while True:
            try:
                item = await asyncio.wait_for(queue.get(), timeout=20)
                await ws.send_json({"type": "alert", "alert": item})
            except asyncio.TimeoutError:
                await ws.send_json({"type": "ping"})
    except WebSocketDisconnect:
        pass
    finally:
        bus.unsubscribe(queue)
