import jwt
from datetime import datetime, timedelta
from app.core.config import settings


class JWT:

    @staticmethod
    def encode(
        payload: dict,
        private_key: str,
        expire_minutes: int | None = None,
        expire_days: int | None = None,
    ) -> str:
        now = datetime.utcnow()
        to_encode = payload.copy()

        if expire_minutes:
            exp = now + timedelta(minutes=expire_minutes)
        else:
            exp = now + timedelta(days=expire_days)

        to_encode.update(
            exp=exp,
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
