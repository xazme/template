from typing import TYPE_CHECKING
from fastapi import Response
from app.token import Tokens
from app.shared import ExceptionRaiser

if TYPE_CHECKING:
    from app.user import User
    from app.token import AccessToken, RefreshToken
    from app.user import IUserRepository
    from app.auth import IPasswordCheker
    from app.token import ITokenService


class AuthService:
    def __init__(
        self,
        user_repo: "IUserRepository",
        password_checker: "IPasswordCheker",
        token_service: "ITokenService",
    ):
        self.user_repo = user_repo
        self.password_checker = password_checker
        self.token_service = token_service

    async def authentificate(self, response: Response):
        user_data: dict = self.user_repo.get_user_data()
        user_username = user_data.get("username")
        user_password = user_data.get("password")

        if len(user_password) or len(user_username) < 3:
            ExceptionRaiser.raise_exception(status_code=499)

        user: "User" = await self.user_getter.get_user_by_name(username=user_username)

        result = self.password_checker.check_password(
            password=user_password, hashed_password=user.password
        )

        if result != True:
            ExceptionRaiser.raise_exception(status_code=488)

        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }

        access_token = self.token_service.generate_access_token(data=user_data)
        refresh_token = self.token_service.generate_refresh_token(data=user_data)

        response.set_cookie(
            key=str(Tokens.REFRESH),
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        print(access_token, refresh_token)
        return access_token, refresh_token
