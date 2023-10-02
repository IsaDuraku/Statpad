from fastapi import FastAPI
import uvicorn
from app.routers import telegrafi, bet

app = FastAPI()

app.include_router(bet.router)
app.include_router(telegrafi.router)


@app.get('/')
def hello():
    return {'message': 'hello'}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
