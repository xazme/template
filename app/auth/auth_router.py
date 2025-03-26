from fastapi import APIRouter, Depends
from app.auth.auth_service import AuthService
from app.user import User
from app.shared import ExceptionRaiser, get_token_service
from app.token import TokenShema
from app.token.token_service import TokenService

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/")
async def auth(
    user: User = Depends(AuthService.auth),
    token_service: TokenService = Depends(get_token_service),
) -> TokenShema:

    if not user:
        ExceptionRaiser.raise_exception(status_code=404)

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

    access_token = token_service.generate_access_token(payload=user_data)
    refresh_token = ""

    return TokenShema(
        access_token=access_token,
        refresh_token=refresh_token,
    )
