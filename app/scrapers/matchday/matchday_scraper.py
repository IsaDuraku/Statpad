import requests
from bs4 import BeautifulSoup
from app.models.matchday import Matchday
from sqlalchemy import delete


# Replace this with the URL of the web page you want to scrape
# Replace with the actual URL

# Send an HTTP GET request to the URL
def scrape_matchday():
    league_names = ["primera_division", "bundesliga", "ligue_1", "serie_a", "premier_league"]
    data_list = []
    for league_name in league_names:
        base_url = f'https://www.besoccer.com/competition/scores/{league_name}'

        html_text = requests.get(base_url).text
        soup = BeautifulSoup(html_text, 'lxml')
        response = requests.get(base_url)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'lxml')

            # Find all div elements with class "match-link p0"
            panels = soup.find_all('div', class_='match-link p0')

            # Iterate through the panels and extract the information
            for panel in panels:
                # Extract data from the JSON-LD script tag
                script_tag = panel.find('script', type='application/ld+json')
                if script_tag:
                    json_data = script_tag.string.strip()
                else:
                    continue

                # Extract other relevant data from the div elements
                league_element = panel.find('div', class_='info-head')
                league = league_element.text.strip() if league_element else ""

                name_1 = panel.find('div', class_='team-name ta-r team_left')
                h_name_element = name_1.find('div', class_='name') if name_1 else None
                h_name = h_name_element.text.strip() if h_name_element else ""

                name_2 = panel.find('div', class_='team-name ta-l team_right')
                a_name_element = name_2.find('div', class_='name') if name_2 else None
                a_name = a_name_element.text.strip() if a_name_element else ""

                time_element = panel.find('p', class_='match_hour time')
                time = time_element.text.strip() if time_element else ""

                date_element = panel.find('div', class_='date-transform date ta-c')
                date = date_element.text.strip() if date_element else ""

                # Extract both images from the 'image-box' div
                image_box = panel.find('a')
                images = image_box.find_all('img')
                h_image = images[0]['src']
                a_image = images[1]['src']

                # Create a dictionary to store the data
                matchday_data = {
                    'league': league,
                    'h_name': h_name,
                    'a_name': a_name,
                    'h_image': h_image,
                    'a_image': a_image,
                    'time': time,
                    'date': date
                }

                # Append the dictionary to the list
                data_list.append(matchday_data)
    return data_list


def delete_all_matchday(session):
    # Delete all records from the Stadiums table
    session.execute(delete(Matchday))
    session.commit()


def insert_matchday_into_database(data_list, session):
    if not data_list:
        return
    delete_all_matchday(session)
    for item in data_list:
        new_matchday = Matchday(
            league=item["league"],
            h_team=item["h_name"],
            a_team=item["a_name"],
            h_image=item["h_image"],
            a_image=item["a_image"],
            time=item["time"],
            date=item["date"]
        )
        session.add(new_matchday)
    session.commit()
