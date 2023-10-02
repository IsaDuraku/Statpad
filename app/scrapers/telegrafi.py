from datetime import datetime
import requests
from bs4 import BeautifulSoup
from app.models.news import News


def scrape_sport_articles(num_pages: int):
    result = []

    for i in range(1, num_pages + 1):
        url = f'https://telegrafi.com/sport/page/{i}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        parent_div = soup.find('div', class_='catgory-latest category-page--listing')
        if parent_div:
            article_blocks = parent_div.find_all('a', class_='post__large')
            articles = []
            for article in article_blocks:
                title = article.find('p', class_='titleArticle').text.strip()
                url = article['href']
                image_src = article.find('img')['src']
                post_date_info = article.find('div', class_='post_date_info').text.strip()
                category_element = article.find('strong', class_='category-name')
                if category_element is not None:
                    category = category_element.text
                else:
                    category = "N/A"
                articles.append({
                    "Title": title,
                    "URL": url,
                    "Image Source": image_src,
                    "Date Posted": post_date_info,
                    "Category": category
                })

            result.extend(articles)
        else:
            return {"error": "The parent div was not found on the page."}

    return {"articles": result}


def save_to_db( results, session):
    if not results:
        return
    for result in results:
        new_article = News(
            title=result["Title"],
            url=result["URL"],
            image_link=result["Image Source"],
            dateposted=result["Date Posted"],
            category=result["Category"],
            date_scraped=datetime.now()
        )
        if session.query(News).filter_by(title=new_article.title).first():
            continue
        session.add(new_article)
    session.commit()
