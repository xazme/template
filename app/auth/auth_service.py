from typing import TYPE_CHECKING
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.shared import user_db_getter
from app.shared import Hasher
from app.user import User

if TYPE_CHECKING:
    from app.user import UserService


class AuthService:

    @staticmethod
    async def auth(
        form: OAuth2PasswordRequestForm = Depends(),
        db: UserService = Depends(user_db_getter),
    ) -> User | None:

        username = form.username
        password = form.password

        user = await db.get_by_name(username=username)

        checker = Hasher(password=password)
        result = checker.check_password(hashed_password=user.password)

        return user if result else None
