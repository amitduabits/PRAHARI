from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app import store
from app.auth import User, assert_write, require_user
from app.services import matcher

router = APIRouter()


class WatchIn(BaseModel):
    source_case_id: str
    entity_type: str = "vehicle"
    plate: str = ""
    name: str = ""
    category: str = ""
    priority: str = "LOW"
    source: str = ""
    notes: str = ""
    gallery_id: str = ""
    embedding_uri: str = ""


@router.get("/api/watchlist")
def list_watchlist(user: User = Depends(require_user)) -> list[dict]:
    return store.list_watchlist()


@router.post("/api/watchlist")
def upsert_watchlist(body: WatchIn, user: User = Depends(require_user)) -> dict:
    assert_write(user)
    store.upsert_watchlist(body.model_dump())
    matcher.reload()
    store.audit(user.username, "watchlist_edit", body.source_case_id)
    return store.get_watchlist_item(body.source_case_id) or body.model_dump()


@router.delete("/api/watchlist/{source_case_id}")
def delete_watchlist(source_case_id: str, user: User = Depends(require_user)) -> dict:
    assert_write(user)
    if source_case_id == "WL-001":
        raise HTTPException(status_code=400, detail="cannot delete WL-001")
    store.delete_watchlist(source_case_id)
    matcher.reload()
    store.audit(user.username, "watchlist_delete", source_case_id)
    return {"deleted": source_case_id}
