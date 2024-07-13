import uuid
from typing import Union

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import crud.user as crud_user
from models.user import User
from schemas.user import UserCreate, User as UserSchema
from database.database import SessionLocal, engine

User.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None]


@app.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=UserSchema)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/", response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)
