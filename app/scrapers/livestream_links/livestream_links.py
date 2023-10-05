import re
from datetime import date
import requests
from bs4 import BeautifulSoup
from app.models.livestream_links import Livestream_links
from sqlalchemy import delete


def scrape_webpage(url):
    # Send an HTTP GET request to the URL to retrieve the webpage content
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')

        # Find the <body> tag
        body_tag = soup.text.split("\n")[:110]  # Split every line individually

        # Initialize a list to store the extracted lines
        extracted_matches = []

        current_date = date.today()
        # me dictionary
        if body_tag:
            # Split the text into lines
            lines = body_tag
            # Process each line
            for line in lines:
                # Check if the line starts with a time format and contains both | and -
                if any(time_str in line for time_str in
                       ["00:", "01:", "02:", "03:", "04:", "05:", "06:", "07:", "08:", "09:",
                        "10:", "11:", "12:", "13:", "14:", "15:", "16:", "17:", "18:", "19:",
                        "20:", "21:", "22:",
                        "23:"]) and '|' in line and 'x' in line and "Handball" not in line and "Rugby" not in line:
                    # Split the line at both | and - symbols
                    parts = re.split(r'\t(.*?)\s*\|\s*', line)
                    parts = [p.strip() for p in parts if p.strip()]  # Remove leading/trailing spaces
                    # extracted_lines.append(parts)
                    # Check if there are at least three elements in parts
                    if len(parts) >= 3:
                        line_dict = {
                            "Time": parts[0].strip(),
                            "Match": parts[1].strip(),
                            "URL": parts[2].strip()
                        }

                        line_dict["DATE"] = current_date.strftime('%d-%m-%Y')
                        extracted_matches.append(line_dict)
                    else:
                        print("Skipping line:", line)

            return extracted_matches

        # Print the extracted mathces
        # for line_dict in extracted_matches:
        #     print("Line:", line_dict)
        # else:
        #     print("Failed to retrieve the webpage. Status code:", response.status_code)


def delete_all_links(session):
    # Delete all records from the Livestream_links table
    session.execute(delete(Livestream_links))
    session.commit()


def insert_links_into_database(extracted_matches, session):
    if not extracted_matches:
        return
    delete_all_links(session)
    for line_dict in extracted_matches:
        new_match = Livestream_links(
            time=line_dict["Time"],
            match=line_dict["Match"],
            url=line_dict["URL"],
            date=line_dict["DATE"]
        )
        session.add(new_match)
    session.commit()

# if __name__ == '__main__':
#     # Input the URL of the webpage you want to process
#     webpage_url = 'https://sportsonline.gl/'
#
#     # Call the function to process the webpage
#     process_webpage(webpage_url)
