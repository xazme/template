from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .user_repo import UserRepository
from .user_service import UserService
from app.database.db_service import DBService


def get_user_repo(oauth2_form: OAuth2PasswordRequestForm = Depends()):
    return UserRepository(
        username=oauth2_form.username,
        password=oauth2_form.password,
    )


def get_user_db(
    session: AsyncSession = Depends(DBService.get_session),
) -> UserService:
    return UserService(session=session)
