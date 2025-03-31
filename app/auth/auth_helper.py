from typing import TYPE_CHECKING
from app.shared import ExceptionRaiser

if TYPE_CHECKING:
    from app.user import UserService, User
    from app.token import Tokens, TokenService
    from app.shared import Roles


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
