import uuid

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: uuid.UUID
    is_active: bool

    class Config:
        from_attributes = True


class UserInDB(User):
    password: str
