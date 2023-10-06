from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from app.models.matches import LiveSoccerScores
from app.scrapers.matches import scrape_and_store_soccer_scores
from app.database import SessionLocal

router = APIRouter(
    prefix='/matches',  # Set the prefix to 'matches'
    tags=['matches']
)

@router.get("/scrape-scores/{date}")
def scrape_and_save_live_scores(date: str):
    try:
        scrape_and_store_soccer_scores(date)
        return {"message": f"Live soccer scores for {date} scraped and saved successfully!"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
@router.get("/scores/")
def get_scores_by_date(date: str = Query(None, title="Date of scores")):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    db = SessionLocal()
    live_scores = db.query(LiveSoccerScores).filter(LiveSoccerScores.match_date == date).all()
    db.close()
    return {"live_scores": live_scores}
