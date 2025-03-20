from typing import List
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from app.user.model import User
from app.user.schema import UserCreate


class UserService:

    @staticmethod
    async def get_all(session: AsyncSession) -> List[User]:
        stmt = select(User).order_by(User.id)
        result: Result = await session.execute(statement=stmt)
        users: List[User] = result.scalars().all()
        return users

    @staticmethod
    async def get_one(session: AsyncSession, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result: Result = await session.execute(statement=stmt)
        user: User | None = result.scalar_one_or_none()
        return user

    @staticmethod
    async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
        user: User = User(**user_data.model_dump())
        try:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
        except IntegrityError:
            await session.rollback()
            raise Exception  # TODO remake
