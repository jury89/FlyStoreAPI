import uuid
import jwt
import crud.user

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from core.config import settings
from dependencies import oauth2_scheme, get_db
from schemas import user
from schemas.token import TokenData
from schemas.user import User

router = APIRouter()


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    db_user = crud.user.get_user_by_email(db, email=token_data.username)

    if db_user is None:
        raise credentials_exception
    return db_user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[user.User, Depends(get_current_active_user)]):
    return current_user


@router.post("/users/", response_model=user.User)
def create_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_data: user.UserCreate,
        db: Session = Depends(get_db)
):
    db_user = crud.user.get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.user.create_user(db=db, user=user_data)


@router.get("/users/{user_id}", response_model=user.User)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/", response_model=list[user.User])
def get_users(db: Session = Depends(get_db)):
    return crud.user.get_users(db)
