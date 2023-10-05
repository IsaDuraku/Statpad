import requests
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
# Initialize the scheduler
scheduler = BackgroundScheduler()

@scheduler.scheduled_job("interval", seconds=6)
def sportnews_scrape():
    requests.get(
        url="http://localhost:8080/sportnews/scrape",
    )

@scheduler.scheduled_job("interval", seconds=8)
def bets_scrape():
    requests.get(
        url="http://localhost:8080/bets/scrapebets"
    )

