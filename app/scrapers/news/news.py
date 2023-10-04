from datetime import datetime
import requests
from bs4 import BeautifulSoup
from app.models.news import News


def scrape_sport_articles():
    result = []
    url = 'https://www.skysports.com/football/news'

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        news_articles = []

        news_items = soup.select('.news-list__item')

        for news_item in news_items:
            title = news_item.select_one('.news-list__headline-link').get_text(strip=True)
            link = news_item.select_one('.news-list__headline-link')['href']
            timestamp = news_item.select_one('.label__timestamp').get_text(strip=True)

            snippet_element = news_item.select_one('.news-list__snippet')
            snippet = snippet_element.get_text(strip=True) if snippet_element else ""

            news_articles.append({
                'title': title,
                'link': link,
                'timestamp': timestamp,
                'snippet': snippet
            })
            result.extend(news_articles)

        result = {"articles": news_articles}

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data from {url}: {e}")

    return result


def save_to_db(results, session):
    if not results:
        return

    for result in results:
        new_article = News(
            title=result["title"],
            url=result["link"],
            dateposted=result['timestamp'],
            snippet=result['snippet'],
            date_scraped=datetime.now()
        )

        if session.query(News).filter_by(title=new_article.title).first():
            continue

        session.add(new_article)

    session.commit()
