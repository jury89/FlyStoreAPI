import uuid

from typing import List, Type
from sqlalchemy.orm import Session
from core.security import verify_password, get_password_hash
from schemas.user import UserCreate
from models.user import User


def get_user(db: Session, user_id: uuid) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[Type[User]]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    password = get_password_hash(user.password)
    db_user = User(id=uuid.uuid4(), email=user.email, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate(db: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(db, email)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user
