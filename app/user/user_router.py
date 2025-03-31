from typing import Annotated
from fastapi import APIRouter, Depends, Path, Query
from app.core.config import settings
from app.user.user_schema import UserResponce, UserCreate, UserUpdate
from app.shared import ExceptionRaiser
from app.shared import HashHelper
from .user_service import UserService
from .user_dependencies import get_user_service


router = APIRouter(prefix=settings.api.user_prefix, tags=["Users"])


@router.get("/")
async def get_all(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_all()


@router.get("/{user_id}")
async def get_user(
    user_id: Annotated[int, Path()],
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get(user_id)
    if not user:
        ExceptionRaiser.raise_exception(status_code=404)
    return UserResponce.model_validate(user)


@router.post("/{user_id}")
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    upd_user_data = user_data.copy()
    upd_user_data.password = HashHelper.hash_password(password=user_data.password)
    user = await user_service.create(upd_user_data.dict())
    if not user:
        ExceptionRaiser.raise_exception(status_code=400)
    return UserResponce.model_validate(user)


@router.put("/{user_id}")
async def update_user(
    user_id: Annotated[int, Path()],
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    updated_user = await user_service.update(
        user_id, user_data.dict(exclude_unset=True)
    )
    if not updated_user:
        ExceptionRaiser.raise_exception(status_code=404)
    return UserResponce.model_validate(updated_user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: Annotated[int, Path()],
    user_service: UserService = Depends(get_user_service),
):
    deleted_user = await user_service.delete(user_id)
    if not deleted_user:
        ExceptionRaiser.raise_exception(status_code=404)
    return {"message": "User deleted successfully"}
