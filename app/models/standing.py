from pydantic import BaseModel
from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LeagueTable(Base):
    __tablename__ = "league_tables"

    id = Column(Integer, primary_key=True, index=True)
    position = Column(String)
    club = Column(String(500))
    points = Column(Integer)

# Pydantic model for input data
class LeagueTableCreate(BaseModel):
    position: str
    club: str
    points: int