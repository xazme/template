from typing import Annotated
from fastapi import APIRouter, Depends
from app.auth.auth_service import AuthService
from app.user import User
from app.shared import ExceptionRaiser

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/")
async def auth(user: User = Depends(AuthService.auth)):

    if not user:
        ExceptionRaiser.raise_exception(status_code=404)

    access_token = ""
    refresh_token = ""

    return ""
