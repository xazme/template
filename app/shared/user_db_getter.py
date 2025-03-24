from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.user.user_service import UserService
from app.database.db_service import DBService


def get_user_db(session: AsyncSession = Depends(DBService.get_session)):
    return UserService(session=session)
