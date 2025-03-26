from typing import AsyncGenerator, TYPE_CHECKING
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db_service import DBService
from app.shared.jwt import JWT


class TokenService:
    def __init__(self, token_url):
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)

    def generate_access_token(
        self,
        payload: dict,
    ) -> str:
        return JWT.encode(payload=payload)

    def generate_refresh_token():
        pass
