import bcrypt


class Hasher:
    def __init__(self, password: str):
        self.password = password.encode()

    def hash_password(self) -> str:
        salt = bcrypt.gensalt()
        return (bcrypt.hashpw(salt=salt, password=self.password)).decode()

    def check_password(self, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=self.password,
            hashed_password=hashed_password.encode(),
        )
