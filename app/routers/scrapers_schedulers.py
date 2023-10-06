import requests
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

@scheduler.scheduled_job("interval", hours=1)
def sportnews_scrape():
    requests.get(
        url="http://localhost:8080/sportnews/scrape",
    )

@scheduler.scheduled_job("interval", hours=1)
def bets_scrape():
    requests.get(
        url="http://localhost:8080/bets/scrapebets"
    )

