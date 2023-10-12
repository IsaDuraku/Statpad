from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.matches import Base as MatchesBase
from app.models.user import Base as UserBase
from app.models.news import Base as NewsBase
from app.models.livestream_links import Base as LSBase
from app.models.highlights import Base as HLBase
from app.models.players import Base as PlayersBase
from app.models.standing import Base as StandingsBase
from app.models.bet import Base as BetBase

from fastapi import FastAPI
from decouple import config

# Initialize FastAPI app
app = FastAPI()

# Configure the database connection
DATABASE_URL = config("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Create tables if they don't exist
NewsBase.metadata.create_all(bind=engine)
MatchesBase.metadata.create_all(bind=engine)
UserBase.metadata.create_all(bind=engine)
LSBase.metadata.create_all(bind=engine)
StandingsBase.metadata.create_all(bind=engine)
PlayersBase.metadata.create_all(bind=engine)
HLBase.metadata.create_all(bind=engine)
BetBase.metadata.create_all(bind=engine)



# Create a session for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

