import requests
from bs4 import BeautifulSoup
import json
import os

def get_data():
    # 1. This "User-Agent" makes the robot look like a real person on a computer
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    table_url = "https://www.kenyanpremierleague.com//kenyan-premier-league/tabelle/wettbewerb/KEN1"
    
    try:
        response = requests.get(table_url, headers=headers, timeout=10)
        # Check if the website blocked us (Status 403 or 404)
        if response.status_code != 200:
            print(f"Blocked by website! Status code: {response.status_code}")
            return [], []

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 2. Look for the table using a more reliable method
        # We look for the div that wraps the table first
        table_div = soup.find("div", class_="responsive-table")
        if not table_div:
            print("Could not find the table div. The website layout might have changed.")
            return [], []

        table = table_div.find("table", class_="items")
        if not table:
            print("Found the div, but the table inside is missing.")
            return [], []

        standings = []
        rows = table.find_all("tr")[1:] # Skip header
        
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 8:
                standings.append({
                    "pos": cols[0].text.strip(),
                    "team": cols[2].text.strip(),
                    "played": cols[3].text.strip(),
                    "gd": cols[8].text.strip(),
                    "pts": cols[9].text.strip()
                })

        # Hardcoded sample players for now (to ensure the file is created)
        players = [
            {"name": "Benson Omala", "team": "Gor Mahia", "market_value": "€150k", "role": "Striker", "history": [{"club": "Gor Mahia"}]},
            {"name": "Austin Odhiambo", "team": "Gor Mahia", "market_value": "€125k", "role": "Midfielder", "history": [{"club": "Gor Mahia"}]}
        ]
        
        return standings, players

    except Exception as e:
        print(f"An error occurred: {e}")
        return [], []

# Ensure the 'data' folder exists
if not os.path.exists('data'):
    os.makedirs('data')

standings, players = get_data()

# Only save if we actually found data
if standings:
    with open('data/standings.json', 'w') as f:
        json.dump(standings, f, indent=2)
    with open('data/players.json', 'w') as f:
        json.dump(players, f, indent=2)
    print("Success! Files updated.")
else:
    print("No data was saved because the table could not be found.")
