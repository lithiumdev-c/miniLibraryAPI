from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from typing import Annotated
from fastapi import Depends

from dotenv import load_dotenv
import os
load_dotenv()

class Base(DeclarativeBase):
    pass

DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise ValueError('DB_URL not found!')

engine = create_async_engine(url=DB_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session

session_dep = Annotated[AsyncSession, Depends(get_db)]