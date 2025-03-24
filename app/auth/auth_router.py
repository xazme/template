from typing import Annotated
from fastapi import APIRouter, Depends
from app.auth.auth_service import AuthService

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post()
async def auth(user=Depends(AuthService.auth)):
    access_token = ""
    refresh_token = ""

    return ""
