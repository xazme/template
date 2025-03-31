class UserRepository:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def get_user_data(self):
        return {"username": self.username, "password": self.password}
