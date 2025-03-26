from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import (
    InvalidSignatureError,
    ExpiredSignatureError,
    DecodeError,
    InvalidAlgorithmError,
    ImmatureSignatureError,
    InvalidAudienceError,
)
from app.shared.jwt import JWT
from app.shared.exceptions import ExceptionRaiser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in", auto_error=False)


def get_users_payload(public_key: str, token: str = Depends(oauth2_scheme)):

    if not token:
        ExceptionRaiser.raise_exception(
            status_code=401,
            detail="Not Authorized. Token is missing",
        )
    try:
        payload = JWT.decode(
            token=token,
            public_key=public_key,
        )

    except ExpiredSignatureError:
        ExceptionRaiser.raise_exception(
            status_code=401,
            detail="Истёкший токен",
        )
    except InvalidSignatureError:
        ExceptionRaiser.raise_exception(
            status_code=401,
            detail="Неверная подпись токена",
        )
    except DecodeError:
        ExceptionRaiser.raise_exception(
            status_code=400,
            detail="Ошибка декодирования токена",
        )
    except InvalidAlgorithmError:
        ExceptionRaiser.raise_exception(
            status_code=400,
            detail="Неверный алгоритм подписи токена",
        )
    except ImmatureSignatureError:
        ExceptionRaiser.raise_exception(
            status_code=401,
            detail="Токен ещё не действителен",
        )
    except InvalidAudienceError:
        ExceptionRaiser.raise_exception(
            status_code=401,
            detail="Неверная аудитория токена",
        )
    except Exception:
        ExceptionRaiser.raise_exception(
            status_code=400,
            detail="Неизвестная ошибка обработки токена",
        )
    return payload
