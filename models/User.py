from sqlalchemy import Column, Uuid, String, Boolean

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Uuid, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_active = Column(Boolean, default=True)
