import uuid
import logging

from sqlalchemy.orm import Session
from . import schemas
from .User import User


def get_user(db: Session, user_id: uuid):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "somehashedpassword"
    db_user = User(id=uuid.uuid4(), email=user.email, password=fake_hashed_password)
    logging.info('User Uuid %s' % db_user.id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logging.info('Refr Uuid %s' % db_user.id)
    return db_user
