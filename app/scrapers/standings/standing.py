from bs4 import BeautifulSoup
import requests
from sqlalchemy import delete

from app.models.standing import LeagueTable  # Assuming this import is correctly defined
from app.models.standing import LeagueTableCreate
from app.database import SessionLocal

import re

def get_league_table():
    league_names = ["primera_division", "bundesliga", "ligue_1", "serie_a", "premier_league"]
    base_url = 'https://www.besoccer.com/competition/table'
    data_dict_list = []

    for league_name in league_names:
        league_url = f'{base_url}/{league_name}'

        html_text = requests.get(league_url).text
        soup = BeautifulSoup(html_text, 'html.parser')

        table = soup.find('table', class_='table')
        rows = table.find_all('tr', class_='row-body')

        for row in rows:
            columns = row.find_all('td')
            position = columns[0].div.text.strip()
            image_url = columns[1].find('img')['src']
            team_name = columns[2].find('span', class_='team-name').text.strip()
            points = columns[3].text.strip()
            matches_played = columns[4].text.strip()
            matches_played = matches_played.split('\n')[0]
            wins = columns[5].text.strip()
            draws = columns[6].text.strip()
            losses = columns[7].text.strip()
            goals_for = columns[8].text.strip()
            goals_against = columns[9].text.strip()
            goal_difference = columns[10].text.strip()

            # Clean the 'matches_played' value to contain only digits
            cleaned_matches_played = re.sub(r'\D', '', matches_played)

            data_dict_list.append({
                'Position': position,
                'ImageURL': image_url,
                'TeamName': team_name,
                'Points': points,
                'MatchesPlayed': int(cleaned_matches_played),  # Convert cleaned value to an integer
                'Wins': wins,
                'Draws': draws,
                'Losses': losses,
                'GoalsFor': goals_for,
                'GoalsAgainst': goals_against,
                'GoalDifference': goal_difference,
            })

    return data_dict_list


def get_club_names_from_leagues():
    league_names = ["la-liga", "bundesliga", "ligue-1", "serie-a", "premier-league"]
    base_url = 'https://www.skysports.com/'
    club_names_list = []

    for league_name in league_names:
        league_url = f'{base_url}{league_name}-table'

        html_text = requests.get(league_url).text
        soup = BeautifulSoup(html_text, 'html.parser')

        table = soup.find('table', class_='standing-table__table')

        if not table:
            continue

        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')
            club_name = columns[1].text.strip()
            club_names_list.append(club_name)

    return club_names_list

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


def save_to_db(data_dict_list, session):
    try:
        for league_data in data_dict_list:
            new_league = LeagueTable(
                position=league_data['Position'],
                imageurl=league_data['ImageURL'],
                club=league_data['TeamName'],
                plays=league_data['MatchesPlayed'],
                wins=league_data['Wins'],
                draws=league_data['Draws'],
                losses=league_data['Losses'],
                goalsscored=league_data['GoalsFor'],
                goalsconceded=league_data['GoalsAgainst'],
                goaldifference=league_data['GoalDifference'],
                points=league_data['Points']
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
