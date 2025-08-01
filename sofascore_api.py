import os
import requests

# Configuración base para RapidAPI SofaScore
BASE_URL = "https://sofascore.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),   # Defínela en Render o local
    "x-rapidapi-host": "sofascore.p.rapidapi.com"
}

# IDs exactos
TOURNAMENT_ID = 406     # Liga 1 Perú Clausura
TEAM_ID = 2305          # Universitario de Deportes
SEASON_ID = 70962       # Temporada Clausura 2025

# -------------------------------
# Funciones de consulta a la API
# -------------------------------

def get_team_fixtures(team_id: int = TEAM_ID, page_index: int = 0):
    """
    Obtiene los próximos partidos de Universitario (o cualquier team_id).
    """
    url = f"{BASE_URL}/teams/get-next-matches"
    params = {"teamId": str(team_id), "pageIndex": str(page_index)}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()


def get_standings(tournament_id: int = TOURNAMENT_ID, season_id: int = SEASON_ID, type_: str = "total"):
    """
    Obtiene la tabla de posiciones del Torneo Clausura 2025.
    """
    url = f"{BASE_URL}/tournaments/get-standings"
    params = {"tournamentId": str(tournament_id), "seasonId": str(season_id), "type": type_}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()