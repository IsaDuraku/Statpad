import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from app.routers import user_routes
from app.routers.matches import matches
from app.routers.scrapers_schedulers import scheduler
from app.routers.bets import bet
from app.routers.news import news
from app.routers.livestream_links import livestream
from app.routers.highlights import highlights
from app.routers import standing

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/app/static", StaticFiles(directory="app/static"), name="static")


app.include_router(user_routes.router, prefix="/api")
app.include_router(bet.router)
app.include_router(news.router)
app.include_router(standing.router)
app.include_router(livestream.router)
app.include_router(highlights.router)
app.include_router(matches.router)


@app.on_event("startup")
async def startup():
    scheduler.start()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
