from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

from datetime import datetime

from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password_hash: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
