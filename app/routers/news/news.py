from fastapi import APIRouter, Query,Request
from fastapi.templating import Jinja2Templates
from app.models.news import News
from app.scrapers.news.news import scrape_sport_articles, save_to_db
from app.database import SessionLocal

router = APIRouter(
    prefix='/sportnews',
    tags=['sportnews']
)
templates=Jinja2Templates(directory='templates')


@router.get("/scrape")
async def scrape():
    db = SessionLocal()
    try:
        scraped_data = scrape_sport_articles()
        save_to_db(scraped_data.get("articles", []), db)
        return {"message": scraped_data}
    except Exception as e:
        db.close()


@router.get("/newsdata")
def read_news(q:str=Query(None)):
    db = SessionLocal()
    if q:
        news=db.query(News).filter(News.title.ilike(f"%{q}%")).all()
    else:
        news = db.query(News).all()
    db.close()
    return news
