from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timezone

from app.models.user import User
from app.schemas.auth import CreateUserSchema

from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher


bcrypt_context = PasswordHash((BcryptHasher(),))

class AuthRepository:
    @classmethod
    async def create_user_model(cls, data: CreateUserSchema, session: AsyncSession):
        create_user_model = User(
        username = data.username,
        email = data.email,
        password_hash = bcrypt_context.hash(data.password), #type: ignore
        created_at = datetime.now(timezone.utc).replace(tzinfo=None)
        )

        session.add(create_user_model)
        await session.commit()
        await session.refresh(create_user_model)

        return create_user_model
    
    @classmethod
    async def authenticate_user(cls, db:AsyncSession, username: str, password: str):
        query = await db.execute(select(User).where(User.username == username))
        user = query.scalar_one_or_none()
        if not user:
            return False
        if not bcrypt_context.verify(password, user.password_hash):
            return False
        
        return user
