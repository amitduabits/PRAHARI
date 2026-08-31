from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel

from app.auth import User, get_user, issue_session, lookup_user, require_roles, require_user
from app import store

router = APIRouter()


class LoginIn(BaseModel):
    username: str
    password: str


@router.post("/api/login")
def login(body: LoginIn, response: Response) -> dict:
    user = lookup_user(body.username, body.password)
    if not user:
        raise HTTPException(status_code=401, detail="bad credentials")
    token = issue_session(user)
    response.set_cookie("prahari_session", token, httponly=True, samesite="lax")
    return {"username": user.username, "role": user.role, "department": user.department}


@router.post("/api/logout")
def logout(response: Response) -> dict:
    response.delete_cookie("prahari_session")
    return {"ok": True}


@router.get("/api/me")
def me(user: User = Depends(require_user)) -> dict:
    return {"username": user.username, "role": user.role, "department": user.department}


@router.get("/api/audit")
def audit_log(user: User = Depends(require_roles("superadmin", "auditor"))) -> list[dict]:
    return store.list_audit()
