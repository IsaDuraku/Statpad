from fastapi import APIRouter, Query, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from app.models.lineup import Lineup, LineupModel
from app.models.form import Form,FormDB
from app.models.form import Form,FormDB
from app.models.team import Team,Team_model
from app.models.user import UserDB
from app.routers.user.security import get_current_user
from app.database import SessionLocal, get_db

router = APIRouter(
    prefix='/myteam',
    tags=['myteam']
)
templates=Jinja2Templates(directory='templates')

# @router.get("/favoriteteam")
# def get_favorite_team(request: Request, user: UserDB = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
#     favorite_team = user.favorite_team
#
#     if not favorite_team:
#         raise HTTPException(status_code=400, detail="User has not set a favorite team")
#
#     lineup = db.query(Lineup).filter(Lineup.team.ilike(f"%{favorite_team}%")).all()
#
#
#     lineup_list = [LineupModel(**item.__dict__) for item in lineup]
#
#     return templates.TemplateResponse("myteam.html", {"request": request, "favorite_team": favorite_team,'lineup':lineup_list})

@router.get('/favoriteteam')
def get_favorite_team(request: Request):
    db = SessionLocal()
    lineup = db.query(Lineup).all()
    forms = db.query(FormDB).all()
    team = db.query(Team).all()
    return templates.TemplateResponse('myteam.html', {
        'request': request,
        'lineup':lineup,
        'team':team,
        'forms':forms
    })