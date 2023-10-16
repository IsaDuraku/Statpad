from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

Base = declarative_base()

class User(BaseModel):
    full_name: Optional[str] = None
    username: str
    email: Optional[str] = None
    password: str
    favorite_team: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class UserDB(Base):  
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_verified = Column(Boolean, default=False)  # New field for email verification
    verification_token = Column(String, unique=True, index=True)
    favorite_team = Column(String, nullable=True)

class UserInDB(User):
    id: int
    created_at: datetime
