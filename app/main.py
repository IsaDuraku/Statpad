import uvicorn
from fastapi import FastAPI
from app.routers import user_routes
from app.routers.bets import bet
from app.routers.news import news
from app.routers import livestream
from app.routers.highlights import highlights

app = FastAPI()

app.include_router(user_routes.router, prefix="/api")
app.include_router(bet.router)
app.include_router(news.router)
app.include_router(livestream.router, prefix="/livestream", tags=["livestream"])
app.include_router(highlights.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

