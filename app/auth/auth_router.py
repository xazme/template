from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Response

from app.user import UserResponce, get_user_service
from app.token import (
    TokenShema,
    Tokens,
    get_token_service,
    get_access_token,
    get_refresh_token,
)
from app.shared import Roles, ExceptionRaiser
from .auth_dependencies import authentificate_user
from .auth_helper import authorize_user

if TYPE_CHECKING:
    from app.token import TokenService, TokenShema
    from app.user import User, UserService, UserResponce


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post(
    "/sign-in",
    response_model=TokenShema,
)
async def auth(
    user: "User" = Depends(authentificate_user),
    token_service: "TokenService" = Depends(get_token_service),
) -> TokenShema:

    user_data: dict = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

    access_token = token_service.generate_access_token(data=user_data)
    refresh_token = token_service.generate_refresh_token(data=user_data)

    return TokenShema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get(
    "/me",
    response_model=UserResponce,
)
async def info(
    token: str = Depends(get_access_token),
    token_service: "TokenService" = Depends(get_token_service),
    user_db: "UserService" = Depends(get_user_service),
):
    user = await authorize_user(
        token=token,
        type=Tokens.ACCESS,
        token_service=token_service,
        user_service=user_db,
        role=Roles.WORKER,
    )

    if not user:
        ExceptionRaiser.raise_exception(status_code=404)
    return UserResponce.model_validate(user)


@router.post(
    "/refresh",
    response_model=TokenShema,
    response_model_exclude_unset=True,
)
async def get_new_access(
    token: str = Depends(get_refresh_token),
    token_service: "TokenService" = Depends(get_token_service),
    user_db: "UserService" = Depends(get_user_service),
):
    user = await authorize_user(
        token=token,
        type=Tokens.REFRESH,
        token_service=token_service,
        user_service=user_db,
        role=Roles.WORKER,
    )
    if not user:
        ExceptionRaiser.raise_exception(status_code=404)

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

    access_token = token_service.generate_access_token(data=user_data)

    return TokenShema(access_token=access_token)
