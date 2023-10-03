from fastapi import FastAPI

app = FastAPI()


def scrape_data():
    # test data
    data = [
        {"team": "Team A", "position": "Forward", "points": 100},
        {"team": "Team B", "position": "Midfielder", "points": 90},
        {"team": "Team C", "position": "Defender", "points": 80},
    ]
    return data

@app.get("/ranklist")
def get_ranklist():
    scraped_data = scrape_data()
    return {"ranklist": scraped_data}
