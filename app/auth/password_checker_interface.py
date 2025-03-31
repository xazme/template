from typing import Protocol


class IPasswordCheker(Protocol):
    def hash_password(self, password: str) -> str: ...

    def check_password(self, password: str, hashed_password: str): ...
