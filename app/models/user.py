from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel


Base = declarative_base()

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str
    full_name: str

class DBUser(Base):  
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    
