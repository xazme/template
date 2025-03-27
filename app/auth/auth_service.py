from typing import TYPE_CHECKING, Protocol
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.shared import get_user_db
from app.shared import Hasher
from app.user import User, UserService

if TYPE_CHECKING:
    from app.user import UserService, User


class AuthService:
    pass
