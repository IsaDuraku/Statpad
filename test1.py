import requests
from bs4 import BeautifulSoup


def scrape_matchday(url):
    data_list = []

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


# Example URL (replace this with the actual URL you want to scrape)
url = 'https://www.besoccer.com/team/manchester-city-fc'

# Call the scrape_matchday function with the URL
matchday_data = scrape_matchday(url)

# Iterate through the list and print the scraped data
for match in matchday_data:
    print("Status:", match['status'])
    print("League:", match['league'])
    print("Home Team Name:", match['h_name'])
    print("Away Team Name:", match['a_name'])
    print("result", match['result'])
    print("Home Team Image:", match['h_image'])
    print("Away Team Image:", match['a_image'])
    print("Date:", match['date'])
    print()