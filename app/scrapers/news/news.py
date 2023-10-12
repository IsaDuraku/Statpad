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
            image_url = news_item.find('img', class_='news-list__image')['data-src']
            context=news_item.find('p',class_='news-list__snippet').get_text(strip=True)
            news_articles.append({
                'title': title,
                'link': link,
                'image_url':image_url,
                'timestamp': timestamp,
                'context':context
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
            image_url=result['image_url'],
            dateposted=result['timestamp'],
            context=result['context'],
            date_scraped=datetime.now()
        )

        if session.query(News).filter_by(title=new_article.title).first():
            continue

        session.add(new_article)

    session.commit()
