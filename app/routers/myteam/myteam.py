from fastapi import APIRouter, Query, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates

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
from app.models.news import News

router = APIRouter(
    prefix='/myteam',
    tags=['myteam']
)
templates=Jinja2Templates(directory='templates')

@router.get('/favoriteteam')
def get_favorite_team(request: Request):
    # Access the auth token directly from the cookies
    auth_token = request.cookies.get("Authorization")

    if not auth_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Fetch user data by making a request to an authentication endpoint
    user_data = fetch_user_data(auth_token)

    if user_data is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    favorite_team = user_data.get("favorite_team")

    db = SessionLocal()

    # Query Lineup with the filter based on the favorite_team
    lineup = db.query(Lineup).filter(Lineup.team.ilike(f"%{favorite_team}%")).all()

    # The rest of your queries
    forms = db.query(FormDB).all()
    team = db.query(Team).all()
    league_table = db.query(LeagueTable).all()
    next_match = db.query(NextMatches).all()
    last_match = db.query(LastMatches).all()
    stadiums = db.query(Stadiums).all()
    news = db.query(News).all()

    # Close the database session
    db.close()

    # Convert the results to LineupModel instances
    lineup_list = [LineupModel(**item.__dict__) for item in lineup]

    return templates.TemplateResponse('myteam.html', {
        'request': request,
        'lineup': lineup_list,
        'team': team,
        'forms': forms,
        'league_table': league_table,
        'next_match': next_match,
        'last_match': last_match,
        'stadiums': stadiums,
        'news': news,
        'favorite_team': favorite_team
    })


# Function to fetch user data by making a request to an authentication endpoint
def fetch_user_data(token):
    import requests

    headers = {"Authorization": token}
    response = requests.get("http://localhost:8080/api/user-profile", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None