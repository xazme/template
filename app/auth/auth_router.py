from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Response

from .auth_dependencies import get_auth_service
from app.user import UserResponce
from app.token import TokenShema

if TYPE_CHECKING:
    from app.token import JWTService, TokenShema
    from app.auth import AuthService
    from app.user import User, UserService, UserResponce


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post(
    "/sign-in",
    response_model=TokenShema,
)
async def auth(
    response: Response,
    auth_service: "AuthService" = Depends(get_auth_service),
) -> TokenShema:

    access_token, refresh_token = await auth_service.authentificate(response=response)

    return TokenShema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


# @router.get(
#     "/me",
#     response_model=UserResponce,
# )
# async def info(
#     token: str = Depends(get_access_token),
#     jwt_service: "JWTService" = Depends(get_jwt_service),
#     user_db: "UserService" = Depends(get_user_db),
# ):
#     user = await get_user_from_token(
#         token=token,
#         type=Tokens.ACCESS,
#         jwt_service=jwt_service,
#         user_db=user_db,
#     )
#     if not user:
#         ExceptionRaiser.raise_exception(status_code=404)
#     return UserResponce.model_validate(user)


# @router.post(
#     "/refresh",
#     response_model=TokenShema,
#     response_model_exclude_unset=True,
# )
# async def get_new_access(
#     token: str = Depends(get_refresh_token),
#     jwt_service: "JWTService" = Depends(get_jwt_service),
#     user_db: "UserService" = Depends(get_user_db),
# ):
#     user = await get_user_from_token(
#         token=token,
#         type=Tokens.ACCESS,
#         jwt_service=jwt_service,
#         user_db=user_db,
#     )
#     if not user:
#         ExceptionRaiser.raise_exception(status_code=404)

#     user_data = {
#         "id": user.id,
#         "username": user.username,
#         "email": user.email,
#     }

#     access_token = jwt_service.generate_access_token(data=user_data)

#     return TokenShema(access_token=access_token)
