from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud.user
from dependencies import get_db
from schemas.user import UserInDB

router = APIRouter()


@router.post("/token")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    print('cacca')
    user_db = crud.user.get_user_by_email(db, form_data.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user = UserInDB.model_validate(user_db)

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.email, "token_type": "bearer"}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password + "somehashedpassword" == hashed_password
