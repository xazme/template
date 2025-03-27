from typing import TYPE_CHECKING
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.user.user_service import UserService
from app.database.db_service import DBService
from app.token import JWTService
from app.core.config import settings
from app.shared import Tokens

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.auth.access_token_url)


def get_user_db(
    session: AsyncSession = Depends(DBService.get_session),
) -> UserService:
    return UserService(session=session)


def get_jwt_service() -> JWTService:
    return JWTService(
        alogrithm=settings.auth.algorithm,
        expire_days=settings.auth.expire_days,
        expire_minutes=settings.auth.expire_days,
        access_private_key=settings.auth.access_private_key,
        access_public_key=settings.auth.access_public_key,
        refresh_private_key=settings.auth.refresh_private_key,
        refresh_public_key=settings.auth.refresh_public_key,
    )


def get_access_token(token: str = Depends(oauth2_scheme)):
    return token


def get_refresh_token(request: Request):
    return request.cookies.get(str(Tokens.REFRESH))


async def get_user_from_token(
    token: str,
    type: Tokens,
    jwt_service: JWTService,
    user_db: UserService,
):

    user_payload = jwt_service.decode(
        token=token,
        type=type,
    )
    user_id = user_payload.get("id")
    user = await user_db.get(id=user_id)

    return user
