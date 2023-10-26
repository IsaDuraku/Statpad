import requests
from bs4 import BeautifulSoup
from app.database import SessionLocal
from app.models.form import FormDB
from sqlalchemy import delete

teams = ['almeria', 'athletic-bilbao', 'atletico-madrid', 'barcelona', 'cadiz', 'celta', 'alaves', 'getafe', 'girona-fc', 'granada', 'ud-palmas', 'mallorca', 'osasuna', 'rayo-vallecano', 'betis', 'real-madrid', 'real-sociedad', 'sevilla', 'valencia-cf', 'villarreal',
             'borussia-dortmund', 'bayer-leverkusen', 'borussia-monchengla', 'bayern-munchen', 'darmstadt-98', 'eintracht-frankfurt', 'fc-augsburg', 'heidenheim', 'tsg-1899-hoffenheim', '1-fc-koln', 'mainz-amat', 'rb-leipzig', 'sc-freiburg', 'stuttgart', '1-fc-union-berlin', 'bochum', 'werder-bremen', 'wolfsburg',
             'clermont-foot', 'havre-ac', 'lens', 'lillestrom', 'lorient', 'metz', 'monaco', 'montpellier-hsc', 'nantes', 'nice', 'olympique-lyonnais', 'olympique-marsella', 'paris-saint-germain-fc', 'stade-brestois-29', 'stade-reims', 'stade-rennes', 'strasbourg', 'toulouse-fc',
             'ac-monza-brianza-1912', 'atalanta', 'bologna', 'cagliari', 'empoli-fc', 'fiorentina', 'frosinone-calcio', 'genoa', 'hellas-verona-fc', 'internazionale', 'juventus-fc', 'lazio', 'lecce', 'milan', 'napoli', 'roma', 'salernitana-calcio-1919', 'us-sassuolo-calcio', 'torino-fc', 'udinese',
             'afc-bournemouth', 'arsenal', 'aston-villa-fc', 'brentford', 'brighton-amp-hov', 'burnley-fc', 'chelsea-fc', 'crystal-palace-fc', 'everton-fc', 'fulham', 'liverpool', 'luton-town-fc', 'manchester-city-fc', 'manchester-united-fc', 'newcastle-united-fc', 'nottingham-forest-fc', 'sheffield-united', 'tottenham-hotspur-fc', 'west-ham-united', 'wolverhampton']


def scrape_form_in_last_matches():
    games_data = []

    for team in teams:
        url = f"https://www.besoccer.com/team/{team}"

        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')

        game_elements = soup.find_all('a', class_='spree-box')
        try:
            team_name = soup.find('h2', class_='title ta-c').text.strip()
        except AttributeError:
            team_name = "Team Name Not Found"  # Provide a default value

        for game_element in game_elements:
            enemy_logo_element = game_element.find('img', class_='shield')
            competition_element = game_element.find('img', class_='league')
            result_element = game_element.find('div', class_='result')

            if enemy_logo_element and competition_element and result_element:
                enemy_logo = enemy_logo_element['src']

                # Extract the logo URL from the src attribute of the competition element
                competition_logo = competition_element['src']

                result = result_element.find_all('span')
                if len(result) >= 2:
                    home_scores = result[0].text.strip()
                    away_scores = result[1].text.strip()
                else:
                    home_scores = "N/A"
                    away_scores = "N/A"

                date_element = game_element.find('div', class_='date')
                date = date_element.text.strip() if date_element else "N/A"

                game_data = {
                    "team_name": team_name,
                    "enemy_logo": enemy_logo,
                    "competition_logo": competition_logo,
                    "date": date,
                    "home_scores": home_scores,
                    "away_scores": away_scores,
                }

                games_data.append(game_data)

    return games_data

def delete_all_games(session):

    session.execute(delete(FormDB))
    session.commit()

def insert_data_into_database(games_data):
    session = SessionLocal()
    delete_all_games(session)

    try:
        if games_data:
            for entry in games_data:
                form_db = FormDB(**entry)
                session.add(form_db)
            session.commit()

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
