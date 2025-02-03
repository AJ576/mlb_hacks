import requests
import json
import pandas as pd


players = pd.read_csv('mlb_players.csv')
dissapeared_players = ['425794','452657','457435','435400','519166','593372','467008','477229','444468','572096']
# # Example: Get Dodgers roster
# url = "https://statsapi.mlb.com/api/v1/people/425794"
# response = requests.get(url)
# data = response.json()
# print(data)

for id in dissapeared_players:
    url = f"https://statsapi.mlb.com/api/v1/people/{id}"
    response = requests.get(url)

    if response.status_code != 200:
        continue  # Skip player if request fails

    data = response.json()
    player = data.get("people", [])[0]  # First player entry

    new_row =  {
        "player_id": player.get("id"),
        "fullName": player.get("fullName", ""),
        "batSide": player.get("batSide", {}).get("code", ""),
        "pitchHand": player.get("pitchHand", {}).get("code", ""),
        "strikeZoneTop": player.get("strikeZoneTop", ""),
        "strikeZoneBottom": player.get("strikeZoneBottom", ""),
    }
    players = players.add(new_row)

players.to_csv("mlb_player_data.csv", index=False)