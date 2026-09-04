from __future__ import annotations

import cv2
import numpy as np
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app import config, store
from app.auth import User, assert_write, require_user
from app.services import faces as faces_mod
from app.services import matcher

router = APIRouter()


@router.get("/api/faces/gallery")
def list_gallery(user: User = Depends(require_user)) -> list[dict]:
    root = config.face_dir()
    out = []
    if root.is_dir():
        for folder in sorted(root.iterdir()):
            if not folder.is_dir():
                continue
            n = len([p for p in folder.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg"}])
            wl = store.get_watchlist_item(folder.name)
            out.append(
                {
                    "gallery_id": folder.name,
                    "name": (wl or {}).get("name") or "",
                    "n_images": n,
                }
            )
    return out


@router.post("/api/faces/enroll")
async def enroll_face(
    gallery_id: str = Form(...),
    name: str = Form(""),
    files: list[UploadFile] = File(default=[]),
    file: UploadFile | None = File(default=None),
    user: User = Depends(require_user),
) -> dict:
    assert_write(user)
    uploads = list(files)
    if file is not None:
        uploads.append(file)
    if not uploads:
        raise HTTPException(status_code=400, detail="no images")
    images = []
    for item in uploads:
        data = await item.read()
        arr = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if frame is not None:
            images.append(frame)
    if not images:
        raise HTTPException(status_code=400, detail="could not decode image")
    result = faces_mod.enroll(gallery_id, images)
    existing = store.get_watchlist_item(gallery_id) or {}
    store.upsert_watchlist(
        {
            "source_case_id": gallery_id,
            "entity_type": "person",
            "plate": existing.get("plate") or "",
            "name": name or existing.get("name") or "",
            "category": existing.get("category") or "MISSING_ASSOCIATE",
            "priority": existing.get("priority") or "HIGH",
            "source": existing.get("source") or "gallery",
            "notes": existing.get("notes") or "",
            "gallery_id": gallery_id,
        }
    )
    matcher.reload()
    store.audit(user.username, "face_enroll", gallery_id)
    return {**result, "name": name}
