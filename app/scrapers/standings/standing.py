from bs4 import BeautifulSoup
import requests
from sqlalchemy import delete

from app.models.standing import LeagueTable  # Assuming this import is correctly defined
from app.models.standing import LeagueTableCreate
from app.database import SessionLocal


def get_league_table():
    league_names = [ "la-liga", "bundesliga", "ligue-1","serie-a","premier-league"]
    base_url = 'https://www.skysports.com/'
    data_dict_list = []

    for league_name in league_names:
        league_url = f'{base_url}{league_name}-table'

        html_text = requests.get(league_url).text
        soup = BeautifulSoup(html_text, 'html.parser')  # Corrected 'htmltext' to 'html_text'

        table = soup.find('table', class_='standing-table__table')  # Corrected class attribute

        if not table:
            continue

        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')
            position = columns[0].text.strip()
            club = columns[1].text.strip()
            pl = columns[2].text.strip()
            w = columns[3].text.strip()
            d = columns[4].text.strip()
            l = columns[5].text.strip()
            f = columns[6].text.strip()
            a = columns[7].text.strip()
            gd = columns[8].text.strip()
            points = columns[9].text.strip()

            data_dict = {
                "Position": position,
                "Club": club,
                "pl": pl,
                "w": w,
                "d": d,
                "l": l,
                "f": f,
                "a": a,
                "gd": gd,
                "Points": points
            }
            data_dict_list.append(data_dict)

    return data_dict_list

def delete_all_data():
        try:
            session = SessionLocal()
            session.execute(delete(LeagueTable))
            session.commit()
        except Exception as e:
            # Handle exceptions or errors that may occur during database operations
            session.rollback()
            raise e
        finally:
            # Always close the session when done
            session.close()

def save_to_db(results, session):
    if not results:
        return

    try:
        for result in results:
            club = result["Club"]
            position = result["Position"]
            pl = result['pl']
            w = result['w']
            d = result['d']
            l = result['l']
            f = result['f']
            a = result['a']
            gd = result['gd']
            points = result["Points"]


            new_league = LeagueTable(
                    club=club,
                    position=position,
                    points=points,
                    plays=pl,
                    wins=w,
                    draws=d,
                    losses=l,
                    goalsscored=f,
                    goalsconceded=a,
                    goaldifference=gd
                )
            session.add(new_league)

        session.commit()
    except Exception as e:
        # Handle exceptions or errors that may occur during database operations
        session.rollback()
        raise e
    finally:
        # Always close the session when done
        session.close()