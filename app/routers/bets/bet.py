from fastapi import APIRouter, HTTPException, Query
from app.models.bet import Bets
from app.scrapers.bets.bet import scrape_bet,save_to_db
from app.database import SessionLocal

router=APIRouter(
    prefix='/bets',
    tags=['bets']
)

@router.get("/scrapebets")
def scrape_and_save_to_db():
    try:
        scraped_data = scrape_bet()
        db = SessionLocal()
        save_to_db(scraped_data['bets'], db)

        return {"message": scraped_data}

    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/betsdata")
def bets_data(q: str = Query(None)):
    db = SessionLocal()
    if q:
        bets = db.query(Bets).filter(Bets.liga.ilike(f"%{q}%")).all()
    else:
        bets = db.query(Bets).all()
    db.close()
    return bets