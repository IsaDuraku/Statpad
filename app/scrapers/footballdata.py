from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Player(BaseModel):
    name: str
    position: str
    points: int


def scrape_data():
    
    data = [
        {"name": "Player 1", "position": "Forward", "points": 100},
        {"name": "Player 2", "position": "Midfielder", "points": 90},
        {"name": "Player 3", "position": "Defender", "points": 80},
    ]
    return [Player(**item) for item in data]

player_router = APIRouter()

@player_router.get("/ranklist", response_model=list[Player])
def get_ranklist():
    scraped_data = scrape_data()
    return scraped_data

app.include_router(player_router, prefix="/players", tags=["players"])
