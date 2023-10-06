from fastapi import APIRouter, HTTPException
from app.models.players import Player
from app.scrapers.players.players import scrape_players, save_player_data_to_db
from app.database import SessionLocal

router = APIRouter(
    prefix='/players',
    tags=['players']
)

league_urls = {
    "Premier League": "https://www.transfermarkt.com/premier-league/scorerliste/wettbewerb/GB1/saison_id/2023/altersklasse/alle",
    "La Liga": "https://www.transfermarkt.com/laliga/torschuetzenliste/wettbewerb/ES1/saison_id/2023",
    "Bundesliga": "https://www.transfermarkt.com/bundesliga/torschuetzenliste/wettbewerb/L1/saison_id/2023",
}

@router.get("/scrapeplayers")
def scrape_and_save_players():
    try:
        scraped_data = {}
        db = SessionLocal()

        for league_name, base_url in league_urls.items():
            player_data_list = scrape_players(league_name)  
            save_player_data_to_db(player_data_list, db, league_name)
            scraped_data[league_name] = f"Scraped and saved {len(player_data_list)} players for {league_name}"

        db.close()
        return {"message": scraped_data}

    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/players")
def players_data(q: str = None):
    db = SessionLocal()
    if q:
        players = db.query(Player).filter(Player.league_name.ilike(f"%{q}%")).all()
    else:
        players = db.query(Player).all()
    db.close()
    return players
