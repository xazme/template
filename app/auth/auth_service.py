import bcrypt
from typing import TYPE_CHECKING, Protocol
from app.user import User, UserService

if TYPE_CHECKING:
    from app.user import UserService, User


class IUserRepository(Protocol):
    def get_user_data(self): ...


class IPasswordCheker(Protocol):
    def check_password(self, password: str, hashed_password: str): ...


class UserRepository:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def get_user_data(self):
        return {"username": self.username, "password": self.password}


class PasswordCheker:
    def __init__(self):
        pass

    def check_password(self, password: str, hashed_password: str):
        return bcrypt.checkpw(
            password=password.encode(), hashed_password=hashed_password.encode()
        )


class AuthService:
    def __init__(
        self,
        user_repo: IUserRepository,
        password_checker: IPasswordCheker,
    ):
        self.user_repo = user_repo
        self.password_checker = password_checker

    async def authentificate(self, user: "User"):
        user_data: dict = self.user_repo.get_user_data()
        user_username = user_data.get("username")
        user_password = user_data.get("password")

        user: "User" = await self.user_getter.get_user_by_name(username=user_username)
        result = self.password_checker.check_password(
            password=user_password, hashed_password=user.password
        )

        return user if result else None
