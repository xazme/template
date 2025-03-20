from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.core.database.service import DBService
from app.user.service.user_service import UserService
from app.user.schema import UserCreate, UserResponce

router = APIRouter(prefix=settings.api.user_prefix, tags=["Users"])


@router.get("/", response_model=list[UserResponce])
async def get_users(
    session: AsyncSession = Depends(DBService.get_session),
) -> list:
    users: list = await UserService.get_all(session=session)
    return users


@router.post("/", response_model=UserResponce)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(DBService.get_session),
):
    user = await UserService.create_user(session=session, user_data=user_data)
    return user
