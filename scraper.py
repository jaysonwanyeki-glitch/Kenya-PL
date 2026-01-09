import requests
from bs4 import BeautifulSoup
import json
import time

def get_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # 1. SCRAPE THE KPL TABLE
    table_url = "https://www.transfermarkt.com/kenyan-premier-league/tabelle/wettbewerb/KEN1"
    table_response = requests.get(table_url, headers=headers)
    table_soup = BeautifulSoup(table_response.content, 'html.parser')
    
    standings = []
    rows = table_soup.find("table", class_="items").find_all("tr")[1:]
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 1:
            standings.append({
                "pos": cols[0].text.strip(),
                "team": cols[2].text.strip(),
                "played": cols[3].text.strip(),
                "gd": cols[8].text.strip(),
                "pts": cols[9].text.strip()
            })

    # 2. SCRAPE TOP PLAYERS (Example: Gor Mahia)
    # Note: In a full version, we'd loop through all teams
    players = [
        {
            "name": "Benson Omala",
            "team": "Gor Mahia",
            "market_value": "€150k",
            "role": "Striker",
            "history": [{"club": "Western Stima"}, {"club": "Gor Mahia"}]
        },
        {
            "name": "Austin Odhiambo",
            "team": "Gor Mahia",
            "market_value": "€125k",
            "role": "Midfielder",
            "history": [{"club": "AFC Leopards"}, {"club": "Gor Mahia"}]
        }
    ]
    
    return standings, players

# SAVE EVERYTHING TO THE DATA FOLDER
standings, players = get_data()

with open('data/standings.json', 'w') as f:
    json.dump(standings, f, indent=2)

with open('data/players.json', 'w') as f:
    json.dump(players, f, indent=2)

print("Robot finished the job!")
