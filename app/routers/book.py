from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated

from sqlalchemy.orm import Session

from app.database import session_dep
from app.models.user import User
from app.repository.book import BookRepository
from app.schemas.book import BookCreateSchema, BookUpdateSchema
from app.repository.user import AuthRepository
from app.repository.book import BookRepository
from app.models.book import Book
from app.routers.auth import get_current_user

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(
    prefix='/books',
    tags=['books']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

@router.post('', status_code=201)
async def create_book(payload:BookCreateSchema, db:session_dep, current_user: Annotated[User, Depends(get_current_user)]):

    book = await BookRepository.create_new_book(payload,owner_id=current_user['id'], db=db) #type: ignore   

@router.get('', status_code=200)
async def show_books(db:session_dep, current_user: Annotated[User, Depends(get_current_user)]):
    books = await BookRepository.show_all_books(db)
    return books

@router.get('/{book_id}:int', status_code=200)
async def show_book(db: session_dep, book_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    book = await BookRepository.show_book(book_id, db) 
    return book

@router.patch('/{book_id}:int')
async def update_book(db: session_dep, payload: BookUpdateSchema, book_id: int, owner_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    updated_book = await BookRepository.patch_book(payload, book_id, owner_id=current_user['id'], db=db) #type: ignore
    return updated_book

@router.delete('/{book_id}:int', status_code=204)
async def delete_id_book(db:session_dep, book_id:int, owner_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    stmt = await BookRepository.delete_book(book_id, owner_id, db)
    if stmt is None:
        raise HTTPException(status_code=404)
    
    return None

@router.post('/{book_id}:int/favourite', status_code=201)
async def add_fav_book(db:session_dep, book_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    fav_book = await BookRepository.add_fav(book_id=book_id, user_id=current_user['id'], db=db) #type: ignore
    
    return fav_book

@router.delete('/{book_id}:int/favourite', status_code=204)
async def del_fav_book(db: session_dep, book_id:int, current_user: Annotated[User, Depends(get_current_user)]):
    BookRepository.delete_book(book_id=book_id, db=db, user_id=current_user['id']) #type: ignore