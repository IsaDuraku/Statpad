
from bs4 import BeautifulSoup
import requests
from app.models.standing import LeagueTable  # Assuming this import is correctly defined
from app.models.standing import LeagueTableCreate
from app.database import SessionLocal


def get_league_table(league_name):
    base_url = 'https://www.skysports.com/'
    league_url = f'{base_url}{league_name}-table'

    html_text = requests.get(league_url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    table = soup.find('table', class_='standing-table__table')
    for tablee in table:
        print(tablee)

    data_dict_list = []

    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')
            position = columns[0].text.strip()
            club = columns[1].text.strip()
            points = columns[9].text.strip()

            data_dict = {
                "Position": position,
                "Club": club,
                "Points": points
            }
            data_dict_list.append(data_dict)
    return data_dict_list
        
def save_to_db(results, session):
    if not results:
        return
    for result in results:
        new_league = LeagueTable(
            club=result["Club"],  # Assuming "Club" is the name of the league
            position=result["Position"],  # You can set the URL if needed
            points=result["Points"]
        )
        session.add(new_league)
    session.commit()






