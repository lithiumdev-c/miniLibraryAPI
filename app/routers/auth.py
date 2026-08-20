from datetime import datetime, timedelta, timezone
from typing import Annotated
from warnings import deprecated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import session

from app.database import async_session, session_dep
from app.models.user import User
from app.schemas.auth import CreateUserSchema, Token
from app.repository.user import AuthRepository

from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = os.getenv('JWT_SECRET')
ALGORITHM = 'HS256'

bcrypt_context = PasswordHash((BcryptHasher(),))
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    expires = datetime.now(timezone.utc) + expires_delta
    encode = {'sub': username, 'id': user_id, 'exp': expires}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM) #type: ignore

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #type: ignore   
        username: str | None = payload.get('sub')
        user_id: int | None = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=401)
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail='Could not validate user.')
    

@router.post('/register', status_code=201)
async def create_user(db: session_dep, payload: CreateUserSchema):
    query = select(User).where(
        User.username == payload.username,
        User.email == payload.email
    )
    res = await db.execute(query)
    exist_user = res.scalar_one_or_none()

    if exist_user:
        raise HTTPException(
            status_code=400
        )

    create_user = await AuthRepository.create_user_model(payload, db)
    return create_user

@router.post('/login', response_model=Token)
async def login(db: session_dep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await AuthRepository.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            headers={'WWW-Auth': "Bearer"}
        )
    token = create_access_token(user.username, user.id, timedelta(minutes=15))

    return {'access_token': token, 'token_type': 'bearer'}
