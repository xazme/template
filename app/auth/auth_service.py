from typing import TYPE_CHECKING
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.shared import get_user_db
from app.shared import Hasher
from app.user import User

if TYPE_CHECKING:
    from app.user import UserService


class AuthService:

    @staticmethod
    async def auth(
        form: OAuth2PasswordRequestForm = Depends(),
        db: "UserService" = Depends(get_user_db),
    ) -> User | None:

        username = form.username
        password = form.password

        user = await db.get_by_name(username=username)

        result = Hasher.check_password(
            password=password,
            hashed_password=user.password,
        )

        return user if result else None
