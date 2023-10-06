import uvicorn
from fastapi import FastAPI
from app.routers import user_routes

from app.routers.scrapers_schedulers import scheduler
from app.routers.bets import bet
from app.routers.news import news
from app.routers.livestream_links import livestream
from app.routers.highlights import highlights
from app.routers import standing

app = FastAPI()

app.include_router(user_routes.router, prefix="/api")
app.include_router(bet.router)
app.include_router(standing.router)


@app.get('/')
def hello():
    return {'message': 'hello'}


app.include_router(news.router)
app.include_router(livestream.router)
app.include_router(highlights.router)
app.include_router(standing.router)


@app.on_event("startup")
async def startup():
    scheduler.start()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
