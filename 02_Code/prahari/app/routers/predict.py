from __future__ import annotations

from fastapi import APIRouter, Depends

from app.auth import User, require_user
from app.services.predict import predict_next

router = APIRouter()


@router.get("/api/predict/{plate}")
def predict(plate: str, user: User = Depends(require_user)) -> dict:
    return predict_next(plate)
