from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.auth import User, require_user
from app.services.query import run

router = APIRouter()


class QueryIn(BaseModel):
    q: str = ""
    limit: int = 50


@router.post("/api/query")
def query(body: QueryIn, user: User = Depends(require_user)) -> dict:
    return run(body.q, limit=body.limit)
