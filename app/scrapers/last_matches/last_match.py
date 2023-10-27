import requests
from bs4 import BeautifulSoup
from sqlalchemy import delete
from app.models.last_match import LastMatches



def scrape_lastmatches():
    team_names = ['almeria']
    data_list = []

    for team_name in team_names:
        url = f'https://www.besoccer.com/team/{team_name}'
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')

            # Find all div elements with class "panel"
            panels = soup.find('div', {'class': 'panel', 'data-cy': 'lastMatch'})

            # Iterate through the panels and extract the information
            if panels:
                # Extract other relevant data from the div elements
                status_1 = panels.find('div', class_='match-status-label')
                status = status_1.text.strip() if status_1 else "FT"
                league_element = panels.find('div', class_='middle-info ta-c')
                league = league_element.text.strip() if league_element else ""

                team_name_elements = panels.find_all('div', class_='name')
                if len(team_name_elements) == 2:
                    h_name = team_name_elements[0].text.strip()
                    a_name = team_name_elements[1].text.strip()
                else:
                    h_name = ""
                    a_name = ""

                team_image_elements = panels.find_all('img')
                if len(team_image_elements) == 2:
                    h_image = team_image_elements[0]['src']
                    a_image = team_image_elements[1]['src']
                else:
                    h_image = ""
                    a_image = ""
                marker = panels.find('div', class_='marker')
                result = marker.text.strip() if marker else "FT"

                date_element = panels.find('div', class_='date-transform date ta-c')
                date = date_element.text.strip() if date_element else ""

                # Create a dictionary to store the data
                matchday_data = {
                    'team_name': team_name,
                    'status': status,
                    'result': result,
                    'league': league,
                    'h_name': h_name,
                    'a_name': a_name,
                    'h_image': h_image,
                    'a_image': a_image,
                    'date': date
                }

                # Append the dictionary to the list
                data_list.append(matchday_data)


    return data_list

def delete_all_lastmatches(session):
    # Delete all records from the Stadiums table
    session.execute(delete(LastMatches))
    session.commit()

def insert_lastmatches_into_database(data_list, session):
    delete_all_lastmatches(session)
    for data in data_list:
        last_match = LastMatches(
            team_name=data['team_name'],
            status=data['status'],
            result=data['result'],
            league=data['league'],
            h_name=data['h_name'],
            a_name=data['a_name'],
            h_image=data['h_image'],
            a_image=data['a_image'],
            date=data['date']
        )
        session.add(last_match)
    session.commit()
