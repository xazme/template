from typing import TYPE_CHECKING, Optional

from fastapi import APIRouter, Depends, Response, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.config import settings
from app.shared import (
    ExceptionRaiser,
    Tokens,
    get_jwt_service,
    get_refresh_token,
    get_access_token,
    get_user_db,
    get_user_from_token,
)
from app.token import JWTService, TokenShema
from app.auth import AuthService, PasswordCheker, UserRepository, UserDB
from app.user import UserResponce

if TYPE_CHECKING:
    from app.user import User, UserService, UserResponce


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post(
    "/sign-in",
    response_model=TokenShema,
)
async def auth(
    response: Response,
    user_data: OAuth2PasswordRequestForm = Depends(),
    user_db: "UserService" = Depends(get_user_db),
    jwt_service: JWTService = Depends(get_jwt_service),
) -> TokenShema:

    user = await user_db.get_by_name(username=user_data.username)
    user.password

    user_repo = UserRepository(username=user_data.username, password=user_data.password)
    password_check = PasswordCheker()

    auth_service = AuthService(
        user_repo=user_repo,
        password_checker=password_check,
    )

    user = await auth_service.authentificate()

    if not user:
        ExceptionRaiser.raise_exception(status_code=401, detail="aa")

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

    access_token = jwt_service.generate_access_token(data=user_data)
    refresh_token = jwt_service.generate_refresh_token(data=user_data)

    response.set_cookie(
        key=str(Tokens.REFRESH),
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

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
    jwt_service: "JWTService" = Depends(get_jwt_service),
    user_db: "UserService" = Depends(get_user_db),
):
    user = await get_user_from_token(
        token=token,
        type=Tokens.ACCESS,
        jwt_service=jwt_service,
        user_db=user_db,
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
    jwt_service: "JWTService" = Depends(get_jwt_service),
    user_db: "UserService" = Depends(get_user_db),
):
    user = await get_user_from_token(
        token=token,
        type=Tokens.ACCESS,
        jwt_service=jwt_service,
        user_db=user_db,
    )
    if not user:
        ExceptionRaiser.raise_exception(status_code=404)

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

    access_token = jwt_service.generate_access_token(data=user_data)

    return TokenShema(access_token=access_token)
