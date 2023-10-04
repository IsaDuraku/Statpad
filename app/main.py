import uvicorn
from fastapi import FastAPI
from app.routers import user_routes
from app.routers import bet
from app.routers import telegrafi
from app.routers import livestream

app = FastAPI()

app.include_router(user_routes.router, prefix="/api")
app.include_router(bet.router)
app.include_router(telegrafi.router)
app.include_router(livestream.router, prefix="/livestream", tags=["livestream"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

