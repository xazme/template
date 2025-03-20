from sqlalchemy.orm import Mapped, mapped_column
from app.core.database.utils import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
