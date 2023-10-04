from fastapi import APIRouter
from app.models.standing import LeagueTable
from app.scrapers.standing import save_to_db,get_league_table
from app.database import SessionLocal
from fastapi import HTTPException


router = APIRouter(
    prefix='/league_table',
    tags=['league_table']
)
@router.post("/scrape/{league_name}")
async def scrape_and_save_to_db(league_name: str):
    db = SessionLocal()

    try:
        scraped_data = get_league_table(league_name)
        if not scraped_data:
            raise HTTPException(status_code=404, detail="League data not found")

        save_to_db(scraped_data, db)
        return {"message": "Data scraped and saved successfully"}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

