import datetime
from pydantic import BaseModel
from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title=Column(String(500))
    url = Column(String(500))
    image_link = Column(String(500))
    dateposted = Column(String(200))
    category = Column(String(200))
    date_scraped = Column(DateTime)

class NewsPydantic(BaseModel):
    id: int
    title:str
    url: str
    image_link: str
    dateposted: str
    category: str
    date_scraped: datetime.datetime


