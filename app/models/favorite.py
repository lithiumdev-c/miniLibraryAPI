from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

from datetime import datetime

class Favourite(Base):
    __tablename__ = 'favourites'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'), unique=True)
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())