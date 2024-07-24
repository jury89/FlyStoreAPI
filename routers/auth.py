import crud.user

from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.config import settings
from core.security import create_access_token
from dependencies import get_db
from schemas.token import Token

router = APIRouter()


@router.post("/token")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
) -> Token:
    user_db = crud.user.authenticate(db, form_data.username, form_data.password)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_db.email}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")
