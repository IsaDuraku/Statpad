from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from app.models.highlights import HighlightsDB
from app.scrapers.highlights.highlights import highlights_scraped, insert_data_into_database
from app.scrapers.highlights.highlights_backup import backup_highlights_scraped
from app.database import SessionLocal



templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix='/highlights',
    tags=['highlights']
)

@router.get("/scrapehighlights")
def scrape_and_save_to_db():
    try:
        scraped_data = highlights_scraped()
        if not scraped_data:
            scraped_data = backup_highlights_scraped() 
            
        db = SessionLocal()
        insert_data_into_database(db, scraped_data)

        return {"message": "Highlights scraped and saved successfully!"}

    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/highlights")
def highlights_data(q: str = Query(None)):
    db = SessionLocal()
    if q:
        highlights = db.query(HighlightsDB).filter(HighlightsDB.competition.ilike(f"%{q}%")).all()
    else:
        highlights = db.query(HighlightsDB).all()
    db.close()
    return highlights

@router.get('/view')
def highlights_view(request: Request, page: int = 1, items_per_page: int = 12):
    db = SessionLocal()

    offset = (page - 1) * items_per_page

    hg = db.query(HighlightsDB).offset(offset).limit(items_per_page).all()

    total_highlights = db.query(HighlightsDB).count()
    total_pages = (total_highlights + items_per_page - 1) // items_per_page

    # Calculate page numbers for pagination
    page_numbers = range(1, total_pages + 1)

    return templates.TemplateResponse('highlights.html',
                                      {
                                          'request': request,
                                          'hg': hg,
                                          'total_pages': total_pages,
                                          'current_page': page,
                                          'page_numbers': page_numbers
                                      })

