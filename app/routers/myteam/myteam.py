from fastapi import APIRouter, Query, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
import pickle
from app.models.last_match import LastMatches
from app.models.lineup import Lineup, LineupModel
from app.models.form import Form,FormDB
from app.models.form import Form,FormDB
from app.models.stadiums import Stadiums
from app.models.standing import LeagueTable
from app.models.team import Team,Team_model
from app.models.team_next_clash import NextMatches
from app.models.user import UserDB
from app.routers.user.security import get_current_user
from app.database import SessionLocal, get_db

router = APIRouter(
    prefix='/myteam',
    tags=['myteam']
)
templates=Jinja2Templates(directory='templates')

@router.get('/favoriteteam')
def get_favorite_team(request: Request):
    db = SessionLocal()
    lineup = db.query(Lineup).all()
    forms = db.query(FormDB).all()
    team = db.query(Team).all()
    league_table = db.query(LeagueTable).all()
    next_match = db.query(NextMatches).all()
    last_match = db.query(LastMatches).all()
    stadiums = db.query(Stadiums).all()
    for team_info in team:
        team_info.team_info = pickle.loads(team_info.team_info)
        team_info.team_performance = pickle.loads(team_info.team_performance)
    return templates.TemplateResponse('myteam.html', {
        'request': request,
        'lineup':lineup,
        'team':team,
        'forms':forms,
        'league_table':league_table,
        'next_match':next_match,
        'last_match':last_match,
        'stadiums':stadiums,
    })