import json

from pydantic import BaseModel
from typing import Dict
from sqlalchemy import Column, String, Text, DateTime, Integer, Sequence
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class LeagueSimulation(Base):
    __tablename__ = "league_simulation"

    id = Column(Integer, primary_key=True, index=True)
    league_winner = Column(String)
    league_name = Column(String)
    team_name = Column(String)
    team_position = Column(Integer)

class LeagueSimulationModel(BaseModel):
    league_winner: str
    team_name: str
    team_position: int
    league_name: str