from typing import Protocol, Dict
from app.token import Tokens, AccessToken, RefreshToken


class ITokenService(Protocol):

    def generate_access_token(self, data: Dict) -> AccessToken: ...

    def generate_refresh_token(self, data: Dict) -> RefreshToken: ...

    def decode(self, token: str, type: Tokens) -> Dict: ...
