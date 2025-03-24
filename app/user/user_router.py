from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.database.db_service import DBService
from app.user.user_schema import UserResponce, UserCreate, UserUpdate
from app.shared import ExceptionRaiser
from app.user.user_service import UserService

router = APIRouter(prefix=settings.api.user_prefix, tags=["Users"])


def get_user_db(session: AsyncSession = Depends(DBService.get_session)):
    return UserService(session=session)


@router.get("/by-id/")
async def get_user(
    user_id: Annotated[int, Query()],
    user_service: UserService = Depends(get_user_db),
):
    user = await user_service.get(user_id)
    if not user:
        ExceptionRaiser.raise_exception(status_code=404)
    return user


@router.get("/by-name/")
async def get_user_by_name(
    username: Annotated[str, Query()],
    user_service: UserService = Depends(get_user_db),
):
    user = await user_service.get_by_name(username)
    if not user:
        ExceptionRaiser.raise_exception(status_code=404)
    return user


@router.get("/all/")
async def get_all(user_service: UserService = Depends(get_user_db)):
    return await user_service.get_all()


@router.post("/")
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_db),
):
    user = await user_service.create(user_data.dict())
    if not user:
        ExceptionRaiser.raise_exception(status_code=400)
    return user


@router.put("/")
async def update_user(
    user_id: Annotated[int, Query()],
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_db),
):
    updated_user = await user_service.update(
        user_id, user_data.dict(exclude_unset=True)
    )
    if not updated_user:
        ExceptionRaiser.raise_exception(status_code=404)
    return updated_user


@router.delete("/")
async def delete_user(
    user_id: Annotated[int, Query()],
    user_service: UserService = Depends(get_user_db),
):
    deleted_user = await user_service.delete(user_id)
    if not deleted_user:
        ExceptionRaiser.raise_exception(status_code=404)
    return {"message": "User deleted successfully"}
