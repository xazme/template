import bcrypt


class PasswordCheker:
    def __init__(self):
        pass

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return (bcrypt.hashpw(salt=salt, password=password.encode())).decode()

    def check_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode(), hashed_password=hashed_password.encode()
        )
