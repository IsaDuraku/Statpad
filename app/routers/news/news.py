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

@router.get('/view')
def view_news(request: Request, page: int = 1, items_per_page: int = 10):
    db = SessionLocal()


    offset = (page - 1) * items_per_page
    limit = items_per_page
    news = db.query(News).slice(offset, offset + limit).all()
    total_news_count = db.query(News).count()

    total_pages = (total_news_count + items_per_page - 1) // items_per_page

    page_numbers = list(range(1, total_pages + 1))

    return templates.TemplateResponse('news.html', {
        'request': request,
        'news': news,
        'page_numbers': page_numbers,
        'current_page': page,
        'total_pages': total_pages
    })