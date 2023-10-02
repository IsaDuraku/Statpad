from fastapi import APIRouter, Query
from app.models.news import News
from app.scrapers.telegrafi import scrape_sport_articles, save_to_db
from app.database import SessionLocal

router = APIRouter(
    prefix='/sportnews',
    tags=['sportnews']
)


@router.get("/scrape/{num_pages}")
async def scrape(num_pages: int):
    if num_pages <= 0:
        return {"error": "Invalid number of pages"}
    db = SessionLocal()
    try:
        scraped_data = scrape_sport_articles(num_pages)
        save_to_db(scraped_data.get("articles", []), db)
        return {"message": scraped_data}
    except Exception as e:
        return {"error": f"Error saving data to the database: {str(e)}"}
    finally:
        db.close()


@router.get("/news")
def read_news(q:str=Query(None)):
    db = SessionLocal()
    if q:
        news=db.query(News).filter(News.title.ilike(f"%{q}%")).all()
    else:
        news = db.query(News).all()
    db.close()
    return news
