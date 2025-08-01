import os
import requests

BASE_URL = "https://sofascore.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),  # Define tu RAPIDAPI_KEY en Render o local
    "x-rapidapi-host": "sofascore.p.rapidapi.com"
}

TEAM_ID = 2305        # Universitario de Deportes
TOURNAMENT_ID = 406   # Liga 1
SEASON_ID = 70962     # Clausura 2025

def get_team_fixtures(team_id: int = TEAM_ID):
    url = f"{BASE_URL}/teams/get-next-matches"
    query = {"teamId": str(team_id), "pageIndex": "0"}
    r = requests.get(url, headers=HEADERS, params=query)
    r.raise_for_status()
    return r.json()

def get_standings(tournament_id: int = TOURNAMENT_ID, season_id: int = SEASON_ID):
    url = f"{BASE_URL}/tournaments/get-standings"
    query = {"tournamentId": str(tournament_id), "seasonId": str(season_id), "type": "total"}
    r = requests.get(url, headers=HEADERS, params=query)
    r.raise_for_status()
    return r.json()
