from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
<<<<<<< Updated upstream
from app.models.matches import Base
=======
from models.news import Base
>>>>>>> Stashed changes
from fastapi import FastAPI
from decouple import config

# Initialize FastAPI app
app = FastAPI()

# Configure the database connection
DATABASE_URL = config("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create a session for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
