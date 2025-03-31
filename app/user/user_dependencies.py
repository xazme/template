from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .user_service import UserService
from app.database.db_service import DBService


def get_user_service(
    session: AsyncSession = Depends(DBService.get_session),
) -> UserService:
    return UserService(session=session)
