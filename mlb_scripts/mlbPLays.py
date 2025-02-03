import requests
import pandas as pd
import json
from tqdm import tqdm

def fetch_game_data(game_pk):
    """Fetch single game data from the MLB API."""
    url = f'https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            print(f"Failed to decode JSON for gamePk: {game_pk}")
            return None
    else:
        return None

def process_game_data(game_data):
    """Extract play-by-play data from the game JSON."""
    try:
        plays = game_data['liveData']['plays']['allPlays']
    except KeyError:
        print("Missing key 'allPlays' in game data.")
        return []

    processed_plays = []

    for play in plays:
        try:
            play_info = {
                "gamePk": game_data['gameData']['game']['pk'],
                "gameDate": game_data['gameData']['datetime']['dateTime'],
                "inning": play['about']['inning'],
                "halfInning": play['about']['halfInning'],
                "playDescription": play['result']['description'],
                "eventType": play['result']['eventType'],
                "batter": play['matchup']['batter']['fullName'],
                "pitcher": play['matchup']['pitcher']['fullName'],
                "batSide": play['matchup']['batSide']['description'],
                "pitchHand": play['matchup']['pitchHand']['description'],
                "outs": play['count']['outs'],
                "balls": play['count']['balls'],
                "strikes": play['count']['strikes'],
            }

            # Add pitch details
            for pitch_event in play['playEvents']:
                if pitch_event['isPitch']:
                    pitch_details = {
                        "pitchType": pitch_event['details'].get('type', {}).get('description', None),
                        "pitchSpeed": pitch_event['pitchData'].get('startSpeed', None),
                        "strikeZoneTop": pitch_event['pitchData'].get('strikeZoneTop', None),
                        "strikeZoneBottom": pitch_event['pitchData'].get('strikeZoneBottom', None),
                        "pitchResult": pitch_event['details']['description'],
                        "isInPlay": pitch_event['details']['isInPlay'],
                        "isStrike": pitch_event['details']['isStrike'],
                        "isBall": pitch_event['details']['isBall'],
                    }
                    combined_play_info = {**play_info, **pitch_details}
                    processed_plays.append(combined_play_info)
        except KeyError as e:
            print(f"Skipping play due to missing key: {e}")

    return processed_plays

def main(start_year=2015, end_year=2023):
    """Main script to fetch and save play-by-play data."""
    all_plays = []
    base_schedule_url = 'https://statsapi.mlb.com/api/v1/schedule/games/'

    for year in range(start_year, end_year + 1):
        print(f"Fetching games for year {year}...")
        params = {
            "sportId": 1,  # MLB
            "season": year,
            "gameType": "R",  # Regular season
        }
        schedule_response = requests.get(base_schedule_url, params=params)

        if schedule_response.status_code != 200:
            print(f"Failed to fetch schedule for {year}.")
            continue

        try:
            schedule_data = schedule_response.json()
            games = [game['gamePk'] for date in schedule_data['dates'] for game in date['games']]
        except KeyError as e:
            print(f"Skipping year {year} due to missing key: {e}")
            continue

        for game_pk in tqdm(games, desc=f"Processing games for {year}"):
            game_data = fetch_game_data(game_pk)
            if game_data:
                plays = process_game_data(game_data)
                all_plays.extend(plays)

    # Convert to DataFrame
    df = pd.DataFrame(all_plays)
    df.dropna(inplace=True)  # Remove rows with missing data

    # Save to CSV
    df.to_csv(f"mlb_plays_{start_year}_{end_year}.csv", index=False)
    print(f"CSV file created: mlb_plays_{start_year}_{end_year}.csv")

if __name__ == "__main__":
    main()
