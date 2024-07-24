from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal
from schemas.user import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token):
    return User(
        email="john@example.com", is_active=True
    )


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return fake_decode_token(token);
