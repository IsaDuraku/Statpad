import requests
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

# @scheduler.scheduled_job("interval", minutes=10)
# def sportnews_scrape():
#     requests.get(
#         url="http://localhost:8080/sportnews/scrape",
#     )
#
# @scheduler.scheduled_job("interval", minutes=5)
# def bets_scrape():
#     requests.get(
#         url="http://localhost:8080/bets/scrapebets"
#     )
@scheduler.scheduled_job("interval", seconds=5)
def matches_scrape():
    requests.get(
        url="http://localhost:8080/matches/scores/"
    )