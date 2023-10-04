from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.scrapers.livestream_links import scrape_webpage, insert_links_into_database
from app.database import SessionLocal


router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/scrape-and-insert")
async def scrape_and_insert(db: Session = Depends(get_db)):
    url = 'https://sportsonline.gl/'  # Replace with the desired URL
    extracted_matches = scrape_webpage(url)
    insert_links_into_database(extracted_matches, db)
    return extracted_matches
