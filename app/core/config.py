import os
import dotenv
from pydantic import BaseModel

dotenv.load_dotenv()


class DataFromEnv:
    """Loaded data from .env"""

    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = int(os.getenv("DB_PORT"))
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_NAME: str = os.getenv("DB_NAME")

    APP_HOST: str = os.getenv("APP_HOST")
    APP_PORT: int = int(os.getenv("APP_PORT"))

    PRIV_KEY_PATH: str = os.getenv("PRIVATE_KEY_PATH")
    PUB_KEY_PATH: str = os.getenv("PUBLIC_KEY_PATH")
    ALGORYTHM: str = os.getenn("ALGORYTHM")


class DataBaseConnection:
    """DataBase data"""

    host: str = DataFromEnv.DB_HOST
    port: int = DataFromEnv.DB_PORT
    user: str = DataFromEnv.DB_USER
    password: str = DataFromEnv.DB_PASS
    name: str = DataFromEnv.DB_NAME

    naming_convention: dict[str, str] = {
        "ix": "ix_%(table_name)s_%(column_0_name)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @classmethod
    def get_db_url(cls):
        return f"postgresql+asyncpg://{cls.user}:{cls.password}@{cls.host}:{cls.port}/{cls.name}"


class RunConfig(BaseModel):
    """Application data"""

    host: str = DataFromEnv.APP_HOST
    port: int = DataFromEnv.APP_PORT


class AuthSettings(BaseModel):
    pass


class ApiPrefix(BaseModel):
    """API prefixes"""

    main_prefix: str = "/api"
    user_prefix: str = "/user"
    # etc


class Settings:
    """Main settings class"""

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DataBaseConnection = DataBaseConnection()


settings = Settings()
