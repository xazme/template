from typing import TYPE_CHECKING
from fastapi import Depends, Form
from app.user.user_dependencies import get_user_service
from app.shared import ExceptionRaiser
from app.shared import HashHelper
from app.token import get_access_token, get_refresh_token, get_token_service, Tokens

if TYPE_CHECKING:
    from app.user import UserService, User
    from app.token import TokenService
    from app.shared import Roles


async def authentificate_user(
    username: str = Form(strict=True),
    password: str = Form(strict=True),
    user_service: "UserService" = Depends(get_user_service),
) -> "User":

    if not isinstance(username, str) or not isinstance(password, str):
        ExceptionRaiser.raise_exception(
            status_code=401,
            detail="Invalid credentials",
        )

    user: "User" = await user_service.get_by_name(username=username)

    if not user:
        ExceptionRaiser.raise_exception(status_code=404, detail="User Not Found")

    result = HashHelper.check_password(password=password, hashed_password=user.password)

    if not result:
        ExceptionRaiser.raise_exception(status_code=401, detail="Invalid credentials")

    return user


async def user_from_refresh_token(
    token=Depends(get_refresh_token),
    user_service: "UserService" = Depends(get_user_service),
    token_service: "TokenService" = Depends(get_token_service),
) -> "User":
    print(token)
    user_data: dict = token_service.decode(token=token, type=Tokens.REFRESH)
    user_id = user_data.get("id")
    user: "User" = await user_service.get(id=user_id)

    if not user:
        ExceptionRaiser.raise_exception(status_code=404, detail="User Not Found")

    return user


async def user_from_access_token(
    token=Depends(get_access_token),
    user_service: "UserService" = Depends(get_user_service),
    token_service: "TokenService" = Depends(get_token_service),
) -> "User":
    user_data: dict = token_service.decode(token=token, type=Tokens.ACCESS)
    user_id = user_data.get("id")
    user: "User" = await user_service.get(id=user_id)

    if not user:
        ExceptionRaiser.raise_exception(status_code=404, detail="User Not Found")

    return user
