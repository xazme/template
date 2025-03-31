from fastapi import Depends
from .auth_service import AuthService
from app.user import get_user_repo
from .password_cheker_dependencies import get_password_cheker
from app.token import get_jwt_service


def get_auth_service():
    return AuthService(
        user_repo=get_user_repo,
        password_checker=get_password_cheker,
        token_service=get_jwt_service,
    )
