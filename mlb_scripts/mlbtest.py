import requests
import json

# Example: Get Dodgers roster
url = "https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
response = requests.get(url)
data = response.json()
print(data)