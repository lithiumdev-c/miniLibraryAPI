from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException

from app.models.favorite import Favourite

from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

bcrypt_context = PasswordHash((BcryptHasher(),))

class FavouriteRepository:
    @classmethod
    async def show_favourites(cls, db:AsyncSession, user_id: int):
        query = select(Favourite).where(Favourite.user_id == user_id)
        res = await db.execute(query)

        return res.scalars().all()