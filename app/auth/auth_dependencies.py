from typing import TYPE_CHECKING
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.user.user_dependencies import get_user_service
from app.shared import ExceptionRaiser
from app.shared import HashHelper

if TYPE_CHECKING:
    from app.user import UserService, User
    from app.token import Tokens, TokenService
    from app.shared import Roles


async def authentificate_user(
    user_service: "UserService" = Depends(get_user_service),
    user_data: OAuth2PasswordRequestForm = Depends(),
) -> "User":
    username = user_data.username
    password = user_data.password

    if not isinstance(username, str) or not isinstance(password, str):
        ExceptionRaiser.raise_exception(status_code=401, detail="Invalid credentials")

    user: "User" = await user_service.get_by_name(username=username)
    result = HashHelper.check_password(password=password, hashed_password=user.password)

    if not user:
        ExceptionRaiser.raise_exception(status_code=404, detail="User Not Found")

    if not result:
        ExceptionRaiser.raise_exception(status_code=401, detail="Invalid credentials")

    return user


async def authorize_user(
    token: str,
    type: "Tokens",
    token_service: "TokenService",
    user_service: "UserService",
    role: "Roles",
) -> "User":

    user_payload = token_service.decode(
        token=token,
        type=type,
    )

    user_id = user_payload.get("id")

    user = await user_service.get(id=user_id)

    if user.role != role:
        ExceptionRaiser.raise_exception(
            status_code=403, detail="You dont have permissions"
        )

    return user
