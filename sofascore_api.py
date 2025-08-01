import os
import requests

# Configuración base para RapidAPI SofaScore
BASE_URL = "https://sofascores.p.rapidapi.com/v1"
HEADERS = {
    "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),   # Tu clave de RapidAPI en Render o local
    "X-RapidAPI-Host": "sofascores.p.rapidapi.com"
}

# IDs exactos
TEAM_ID = 406           # Universitario de Deportes
TOURNAMENT_ID = 2305    # Liga 1 Perú Clausura
SEASON_ID = 70962       # Temporada Clausura 2025

# -------------------------------
# Funciones de consulta a la API
# -------------------------------

def get_team_fixtures(team_id: int = TEAM_ID):
    """
    Obtiene los próximos partidos de Universitario (o cualquier team_id).
    """
    url = f"{BASE_URL}/teams/{team_id}/events"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def get_standings(tournament_id: int = TOURNAMENT_ID, season_id: int = SEASON_ID):
    """
    Obtiene la tabla de posiciones del Torneo Clausura 2025.
    """
    url = f"{BASE_URL}/unique-tournaments/{tournament_id}/seasons/{season_id}/standings"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()