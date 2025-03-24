import bcrypt


def hash_password(password: str):
    salt = bcrypt.gensalt()
    return str(
        bcrypt.hashpw(
            salt=salt,
            password=password.encode(),
        )
    )


def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hash_password.encode(),
    )
