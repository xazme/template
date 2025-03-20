from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine
from app.core.database.utils import DBUtils, Base
from app.user.model import User


class DBService:

    engine: AsyncEngine = DBUtils.get_db_engine()

    session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
    )

    @classmethod
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        """Session getter"""
        async with cls.session() as session:
            yield session

    @classmethod
    async def create_tables(cls) -> None:
        """Create Tables"""

        async with cls.engine.begin() as con:
            await con.run_sync(Base.metadata.create_all)

    @classmethod
    async def drop_tables(cls) -> None:
        """Delete Tables"""
        async with cls.engine.begin() as con:
            await con.run_sync(Base.metadata.drop_all)
