from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from starlette.templating import Jinja2Templates

from app import database, models
from app.models import publisher
from app.database import get_db
from app.database import SessionLocal
from app.models.publisher import Publisher_Model, Magazine_Model, Publisher, Magazine



router = APIRouter()

templates = Jinja2Templates(directory="templates")


router = APIRouter(
    prefix='/magazine_publishers'
)

# Dependency to get database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations for Publisher

@router.post("/publishers/")
def create_publisher(publisher: Publisher_Model, db: Session = Depends(get_db)):
    db_publisher = Publisher(**publisher.dict())
    db.add(db_publisher)
    db.commit()
    db.refresh(db_publisher)
    return db_publisher


# CRUD operations for Magazine

@router.post("/magazines/")
def create_magazine(magazine: Magazine_Model, db: Session = Depends(get_db)):
    db_magazine = Magazine(**magazine.dict())
    db.add(db_magazine)
    db.commit()
    db.refresh(db_magazine)
    return db_magazine


@router.get("/magazines/{magazine_type}")
def read_magazine(magazine_type: str, db: Session = Depends(get_db)):
    db_magazine = db.query(Magazine).filter(Magazine.type == type).first()
    if db_magazine is None:
        raise HTTPException(status_code=404, detail="Magazine not found")
    return db_magazine

@router.get("/publishers/read")
def read_publisher(publisher_id: int, db: Session = Depends(get_db)):
    db_publisher = db.query(Publisher).all()
    if db_publisher is None:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return db_publisher

@router.get("/magazines/read")
def read_magazines(db: Session = Depends(get_db)):
    db_magazines = db.query(Magazine).all()
    if not db_magazines:
        raise HTTPException(status_code=404, detail="No magazines found")
    return templates.TemplateResponse("livestream.html", {"magazines": db_magazines})

@router.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("livestream.html", {"request": request})

@router.delete("/magazines/{magazine_id}")
def delete_magazine(magazine_id: int, db: Session = Depends(get_db)):
    db_magazine = db.query(Magazine).filter(Magazine.id == magazine_id).first()
    if db_magazine is None:
        raise HTTPException(status_code=404, detail="Magazine not found")
    db.delete(db_magazine)
    db.commit()
    return {"message": "Magazine deleted successfully"}