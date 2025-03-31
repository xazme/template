from typing import Protocol


class IUserRepository(Protocol):
    def get_user_data(self): ...
