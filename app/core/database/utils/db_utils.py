from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
)
from app.config import settings


class DBUtils:
    """SQLAlchemy engine generator"""

    engine: AsyncEngine = create_async_engine(
        url=settings.db.get_db_url(),
        echo=True,
        pool_size=10,
        max_overflow=20,
    )

    @classmethod
    def get_db_engine(cls) -> AsyncEngine:
        return cls.engine

    @classmethod
    async def dispose(cls):
        await cls.get_db_engine().dispose()


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models"""

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
