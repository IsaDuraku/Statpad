from fastapi import APIRouter
from app.scrapers.livestream_links.livestream_links import scrape_webpage, insert_links_into_database
from app.database import SessionLocal
from app.models.livestream_links import Livestream_links


router = APIRouter(
    prefix='/livestream_scraper',
    tags=['Livestream_links']
)


@router.get("/scrape-and-insert")
async def scrape_and_insert():
    db = SessionLocal()
      # Replace with the desired URL
    extracted_matches = scrape_webpage()
    insert_links_into_database(extracted_matches, db)
    return extracted_matches
#ndreqe qeto posht
@router.get("/get-links-fromDb")
async def get_matches():
    db = SessionLocal()
    matches = db.query(Livestream_links).all()
    return matches

