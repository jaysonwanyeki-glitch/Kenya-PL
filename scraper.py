import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_kenyan_league():
    # Headers to make the bot look like a real person browsing
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Target URL (Example: KPL on Transfermarkt)
    url = "https://www.transfermarkt.com/kenyan-premier-league/startseite/wettbewerb/KEN1"
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        all_data = []
        
        # 1. Find the table containing Teams
        table = soup.find("table", class_="items")
        rows = table.find_all("tr", class_=["odd", "even"])

        for row in rows:
            team_cell = row.find("td", class_="hauptlink no-border-links")
            if team_cell:
                team_name = team_cell.text.strip()
                team_url = "https://www.transfermarkt.com" + team_cell.find("a")['href']
                
                print(f"Fetching players for: {team_name}...")
                
                # 2. Go into each team to get players
                team_response = requests.get(team_url, headers=headers)
                team_soup = BeautifulSoup(team_response.content, 'html.parser')
                
                player_rows = team_soup.find_all("tr", class_=["odd", "even"])
                
                for p_row in player_rows:
                    name_cell = p_row.find("td", class_="hauptlink")
                    value_cell = p_row.find("td", class_="rechts hauptlink")
                    
                    if name_cell and value_cell:
                        player_name = name_cell.text.strip()
                        market_value = value_cell.text.strip() or "N/A"
                        role = p_row.find_all("td")[4].text.strip() # Position
                        
                        # Add to our database
                        all_data.append({
                            "name": player_name,
                            "team": team_name,
                            "market_value": market_value,
                            "role": role,
                            "history": [
                                {"year": "2024", "club": "Previous Club Info (Available in Full Scan)"},
                                {"year": "2025", "club": team_name}
                            ]
                        })
                
                # Small delay to avoid getting banned
                time.sleep(2)

        return all_data

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Execute and Save
data = scrape_kenyan_league()
if data:
    with open('data/players.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Successfully updated {len(data)} players!")
