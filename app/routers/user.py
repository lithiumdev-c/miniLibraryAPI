from fastapi import APIRouter, status, HTTPException, Depends
from typing import Annotated, Any

from app.database import session_dep
from app.models.user import User
from app.routers.auth import get_current_user
from app.repository.favorite import FavouriteRepository

router = APIRouter(
    prefix='/users',
    tags=['users']
)

user_dep = Annotated[dict[str, Any], Depends(get_current_user)]

@router.get('/me', status_code=200)
async def my_account(user: user_dep, db:session_dep):
    return {"Account": user}

@router.get('/me/favourites', status_code=200)
async def my_favs(db: session_dep, current_user: Annotated[User, Depends(get_current_user)]):
    favs = await FavouriteRepository.show_favourites(db=db, user_id=current_user['id']) #type: ignore
    return favs