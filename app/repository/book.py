from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import query

from app.models import book
from app.models import user
from app.models.book import Book
from app.models.favorite import Favourite
from app.models.user import User
from app.schemas.book import BookCreateSchema, BookResponseSchema, BookUpdateSchema

from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher


bcrypt_context = PasswordHash((BcryptHasher(),))

class BookRepository:
    @classmethod
    async def create_new_book(cls, payload: BookCreateSchema, db:AsyncSession, owner_id: int):
        book = Book(**payload.model_dump(), owner_id=owner_id)

        db.add(book)

        await db.commit()
        await db.refresh(book)

        return book

    @classmethod
    async def show_all_books(cls, db:AsyncSession):
        query = select(Book)
        res = await db.execute(query)

        return res.scalars().all()
    
    @classmethod
    async def show_book(cls, book_id:int, db:AsyncSession):
        query = select(Book).where(Book.id == book_id)
        res = await db.execute(query)
        return res.scalar_one_or_none()
    
    @classmethod
    async def patch_book(cls, payload: BookUpdateSchema, book_id:int, owner_id:int, db:AsyncSession):
        query = select(Book).where(Book.id == book_id, Book.owner_id == owner_id)
        res = await db.execute(query)
        book = res.scalar_one_or_none()

        if not book:
            raise HTTPException(
                status_code=404
            )
        
        update_dict = payload.model_dump()

        for key, val in update_dict.items():
            setattr(book, key, val)
        
        await db.commit()
        await db.refresh(book)

        return book
    
    @classmethod
    async def delete_book(cls, book_id: int, owner_id: int, db:AsyncSession):
        stmt = delete(Book).filter(Book.id == book_id, Book.owner_id == owner_id)

        await db.execute(stmt)
        await db.commit()
    
    @classmethod
    async def add_fav(cls, book_id:int, user_id:int, db:AsyncSession):
        query = await db.execute(select(Book).where(Book.id == book_id))
        book = query.scalar_one_or_none()

        if not book:
            raise HTTPException(
                status_code=404
            )
        
        favourite_query = await db.execute(select(Favourite).where(Favourite.user_id == user_id))
        favourite = favourite_query.scalar_one_or_none()

        if favourite:
            raise HTTPException(
                status_code=409,
            )
        
        new_fav = Favourite(user_id=user_id, book_id=book_id)
        db.add(new_fav)

        await db.commit()
        await db.refresh(new_fav)

        return new_fav
    
    @classmethod
    async def delete_fav(cls, book_id: int, user_id: int, db:AsyncSession):
        stmt = delete(Favourite).where(
            Favourite.book_id == book_id,
            Favourite.user_id == user_id
        )

        result = await db.execute(stmt)

        if result.rowcount == 0: #type: ignore
            raise(
                HTTPException(
                    status_code=404
                )
            )
        
        await db.commit()
        return None