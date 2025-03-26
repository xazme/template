from app.token.token_service import TokenService
from app.core.config import settings


def get_token_service() -> TokenService:
    return TokenService(token_url=settings.auth.token_url)
