import requests
import pandas as pd

# Function to get all players
def get_all_players():
    url = "https://statsapi.mlb.com/api/v1/sports/1/players"  # MLB players
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching players list")
        return []

    data = response.json()
    return [player["id"] for player in data.get("people", [])]

# Function to fetch player stats
def get_player_info(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return None  # Skip player if request fails

    data = response.json()
    player = data.get("people", [])[0]  # First player entry

    return {
        "player_id": player.get("id"),
        "fullName": player.get("fullName", ""),
        "batSide": player.get("batSide", {}).get("code", ""),
        "pitchHand": player.get("pitchHand", {}).get("code", ""),
        "strikeZoneTop": player.get("strikeZoneTop", ""),
        "strikeZoneBottom": player.get("strikeZoneBottom", ""),
    }

# Get all player IDs
player_ids = get_all_players()
print(f"Found {len(player_ids)} players.")

# Fetch stats for all players
players_data = [get_player_info(pid) for pid in player_ids]
players_data = [p for p in players_data if p]  # Remove failed fetches

# Convert to DataFrame
df = pd.DataFrame(players_data)

# Save to CSV
csv_filename = "mlb_players_filtered.csv"
df.to_csv(csv_filename, index=False)

print(f"Saved {len(df)} player records to {csv_filename}")
