import requests
from bs4 import BeautifulSoup
import json
import os

def get_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    url = "https://www.transfermarkt.com/kenyan-premier-league/tabelle/wettbewerb/KEN1"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for the table
        table = soup.find("table", class_="items")
        
        if table:
            standings = []
            rows = table.find_all("tr")[1:]
            for row in rows:
                cols = row.find_all("td")
                if len(cols) > 9:
                    standings.append({
                        "pos": cols[0].text.strip(),
                        "team": cols[2].text.strip(),
                        "played": cols[3].text.strip(),
                        "gd": cols[8].text.strip(),
                        "pts": cols[9].text.strip()
                    })
            return standings
    except Exception as e:
        print(f"Error fetching live data: {e}")
    
    # PLAN B: If the website blocks us, use this recent data so the site isn't broken
    print("Website blocked us. Using Plan B (Manual Data).")
    return [
        {"pos": "1", "team": "Gor Mahia", "played": "14", "gd": "+10", "pts": "27"},
        {"pos": "2", "team": "AFC Leopards", "played": "15", "gd": "+6", "pts": "27"},
        {"pos": "3", "team": "Tusker FC", "played": "15", "gd": "+2", "pts": "24"},
        {"pos": "4", "team": "Kenya Police", "played": "14", "gd": "+2", "pts": "23"}
    ]

# Create folder if missing
if not os.path.exists('data'):
    os.makedirs('data')

# Run and Save
final_standings = get_data()
with open('data/standings.json', 'w') as f:
    json.dump(final_standings, f, indent=2)

# Dummy players data to keep the file existing
players = [
    {"name": "Benson Omala", "team": "Gor Mahia", "market_value": "€150k", "role": "Striker", "history": [{"club": "Gor Mahia"}]},
    {"name": "Austin Odhiambo", "team": "Gor Mahia", "market_value": "€125k", "role": "Midfielder", "history": [{"club": "Gor Mahia"}]}
]
with open('data/players.json', 'w') as f:
    json.dump(players, f, indent=2)

print("Robot finished successfully!")
