from fastapi import FastAPI
from app.routers import user_routes

app = FastAPI()

app.include_router(user_routes.router, prefix="/api")


