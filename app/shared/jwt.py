import jwt
from datetime import datetime, timedelta
from app.core.config import settings


class JWT:

    @staticmethod
    def encode(
        payload: dict,
        private_key: str,
        expire_minutes: int = settings.auth.expire_minutes,
    ) -> str:
        now = datetime.utcnow()
        to_encode = payload.copy()

        to_encode.update(
            exp=now + timedelta(minutes=expire_minutes),
            iat=now,
        )

        return jwt.encode(
            payload=to_encode,
            key=private_key,
            algorithm=settings.auth.algorithm,
        )

    @staticmethod
    def decode(
        token: str,
        public_key: str,
    ) -> dict:
        return jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=[settings.auth.algorithm],
        )


# TODO:СОЗДАТЬ 2 ПРИВАТ И ПУБЛ КЛЮЧА
