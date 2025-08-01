import os
import requests

BASE_URL = "https://sofascore.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
    "X-RapidAPI-Host": "sofascore.p.rapidapi.com"
}

TEAM_ID = 2305        # Universitario de Deportes
TOURNAMENT_ID = 406   # Liga 1
SEASON_ID = 70962     # Clausura 2025


def get_team_fixtures(team_id: int = TEAM_ID):
    url = f"{BASE_URL}/teams/get-next-matches"
    params = {"teamId": team_id, "pageIndex": "0"}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()


def get_standings(tournament_id: int = TOURNAMENT_ID, season_id: int = SEASON_ID):
    url = f"{BASE_URL}/tournaments/get-standings"
    params = {"tournamentId": tournament_id, "seasonId": season_id, "type": "total"}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()


def get_team_logo(team_id: int):
    """
    Retorna la URL del logo oficial del equipo.
    """
    url = f"{BASE_URL}/teams/get-logo"
    params = {"teamId": team_id}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json().get("url")  # la API devuelve { "url": "..." }
