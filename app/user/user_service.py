from sqlalchemy import Select, Result
from sqlalchemy.exc import IntegrityError
from app.user.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.table = User

    async def get(self, id: int) -> User | None:
        stmt = Select(self.table).where(self.table.id == id).limit(1)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, username: str) -> User | None:
        stmt = Select(self.table).where(self.table.username == username).limit(1)
        result: Result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list:
        stmt = Select(self.table.username, self.table.id, self.table.last_activity)
        result: Result = await self.session.execute(statement=stmt)
        rows = result.all()
        return [
            {"username": row.username, "id": row.id, "last_activity": row.last_activity}
            for row in rows
        ]

    async def create(self, data: dict) -> User | None:
        user = self.table(**data)
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user

        except IntegrityError:
            await self.session.rollback()
            return None

    async def update(self, user_id: int, new_data: dict):
        user = await self.get(id=user_id)

        if user is None:
            return None

        for key, value in new_data.items():
            setattr(user, key, value)
        return True

    async def delete(self, user_id: int):
        user = await self.get(id=user_id)

        if user is None:
            return None

        await self.session.delete(user)
        await self.session.commit()
        return True
