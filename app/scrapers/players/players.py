import requests
from bs4 import BeautifulSoup
from app.models.players import Player

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Referer': 'https://www.google.com',
}

def scrape_players(league_name, num_pages=1, max_players=15):
    base_urls = {
        "Premier League": "https://www.transfermarkt.com/premier-league/scorerliste/wettbewerb/GB1/saison_id/2023/altersklasse/alle",
        "La Liga": "https://www.transfermarkt.com/laliga/torschuetzenliste/wettbewerb/ES1/saison_id/2023",
        "Bundesliga": "https://www.transfermarkt.com/bundesliga/torschuetzenliste/wettbewerb/L1/saison_id/2023",
    }

    base_url = base_urls.get(league_name)

    if base_url is None:
        return []  # Return an empty list if the league name is not found

    all_players = []
    rank = 0

    print(f"Scraping data for {league_name} from URL: {base_url}")  # Add this line

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        h1_element = soup.find('h1', class_='content-box-headline')

        table_title = h1_element.get_text(strip=True)

        print(f"{table_title} ({league_name})")

        table = soup.find('table', {'class': 'items'})

        tr_elements = table.find_all('tr', class_=['even', 'odd'])

        for tr_element in tr_elements:
            rank += 1

            player_img_element = tr_element.find('img', class_='bilderrahmen-fixed')
            if player_img_element and 'data-src' in player_img_element.attrs:
                player_img_url = player_img_element['data-src']
            else:
                player_img_url = "Player image not found"

            player_name_element = tr_element.find_all('a', title=True)[0]
            player_name = player_name_element.text.strip()

            club_name = tr_element.find_all('a', title=True)[1]['title']

            goals_elements = tr_element.find_all('td', class_='zentriert')
            if len(goals_elements) > 4:
                goals = goals_elements[4].text.strip()
            else:
                goals = "0"

            player_data = {
                "Rank": rank,
                "Player Image URL": player_img_url,
                "Player Name": player_name,
                "Club Name": club_name,
                "Goals": goals,
            }

            all_players.append(player_data)

            if rank >= max_players:
                break  
    else:
        print(f"Failed to retrieve the {league_name} web page")

    return all_players

# Rest of your code...


def save_player_data_to_db(player_data_list, session, league_name):
    if not player_data_list:
        return

    for player_data in player_data_list:
        new_player = Player(
            rank=player_data["Rank"],
            player_image_url=player_data["Player Image URL"],
            player_name=player_data["Player Name"],
            club_name=player_data["Club Name"],
            goals=player_data["Goals"],
            league_name=league_name,
        )

        # Check if a player with the same name already exists in the database
        existing_player = session.query(Player).filter_by(player_name=new_player.player_name).first()

        if existing_player:
            continue  # Skip adding duplicate players

        session.add(new_player)

    session.commit()
    print(f"Saved {len(player_data_list)} players to the database for {league_name}")