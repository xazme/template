from fastapi import APIRouter, Depends, Response
from app.auth.auth_service import AuthService
from app.user import User
from app.shared import ExceptionRaiser
from app.token import TokenShema, get_users_payload
from app.shared.jwt import JWT
from app.core.config import settings
from app.shared import get_user_db
from app.user import UserService, UserResponce

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post(
    "/sign-in",
    response_model=TokenShema,
)
async def auth(
    response: Response,
    user: User = Depends(AuthService.auth),
) -> TokenShema:

    if not user:
        ExceptionRaiser.raise_exception(status_code=404)

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

    access_token = JWT.encode(
        payload=user_data,
        private_key=settings.auth.access_private_key,
        expire_minutes=settings.auth.expire_minutes,
    )
    refresh_token = JWT.encode(
        payload=user_data,
        private_key=settings.auth.refresh_private_key,
        expire_days=settings.auth.expire_days,
    )

    response.set_cookie(
        key="Refresh",
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
    user_payload: dict = Depends(
        get_users_payload(public_key=settings.auth.access_public_key)
    ),
    user_service: UserService = Depends(get_user_db),
):
    user_id = user_payload.get("id")
    user: User = await user_service.get(id=user_id)
    return UserResponce.model_validate(user)


@router.post("/refresh", response_model=TokenShema)
async def get_new_access(
    user_service: UserService = Depends(get_user_db),
    user_payload: dict = Depends(
        get_users_payload(public_key=settings.auth.refresh_public_key)
    ),
):
    user_id = user_payload.get("id")
    user: User = await user_service.get(id=user_id)

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

    access_token = JWT.encode(
        payload=user_data,
        private_key=settings.auth.access_private_key,
        expire_minutes=settings.auth.expire_minutes,
    )

    token_data = TokenShema(access_token=access_token)

    return token_data.dict(exclude_unset=True)
