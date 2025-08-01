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

# Carpeta donde guardamos logos
LOGO_DIR = os.path.join("static", "img", "logos")
os.makedirs(LOGO_DIR, exist_ok=True)


def get_team_fixtures(team_id: int = TEAM_ID, page_index: int = 0):
    """
    Obtiene los próximos partidos de Universitario (con logos locales).
    """
    url = f"{BASE_URL}/teams/get-next-matches"
    params = {"teamId": team_id, "pageIndex": page_index}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    events = r.json().get("events", [])

    # Agregamos los logos
    for match in events:
        match["homeTeam"]["logo"] = get_team_logo(match["homeTeam"]["id"])
        match["awayTeam"]["logo"] = get_team_logo(match["awayTeam"]["id"])

    return events


def get_standings(tournament_id: int = TOURNAMENT_ID, season_id: int = SEASON_ID):
    """
    Obtiene la tabla de posiciones (con logos locales).
    """
    url = f"{BASE_URL}/tournaments/get-standings"
    params = {"tournamentId": tournament_id, "seasonId": season_id, "type": "total"}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    data = r.json()

    try:
        standings = data["standings"][0]["rows"]
        for row in standings:
            team_id = row["team"]["id"]
            row["team"]["logo"] = get_team_logo(team_id)
    except Exception as e:
        print(f"Error procesando standings: {e}")

    return data

def get_team_past_matches(team_id: int = TEAM_ID, page_index: int = 0):
    """
    Obtiene los últimos partidos jugados por Universitario (con logos).
    """
    url = f"{BASE_URL}/teams/get-last-matches"
    params = {"teamId": team_id, "pageIndex": page_index}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    events = r.json().get("events", [])

    # Agregar logos
    for match in events:
        try:
            match["homeTeam"]["logo"] = get_team_logo(match["homeTeam"]["id"])
            match["awayTeam"]["logo"] = get_team_logo(match["awayTeam"]["id"])
        except Exception:
            match["homeTeam"]["logo"] = "/static/img/logo_u.png"
            match["awayTeam"]["logo"] = "/static/img/logo_u.png"

    return events


def get_team_logo(team_id: int):
    """
    Descarga el logo del equipo desde SofaScore y lo guarda en static/img/logos/.
    Devuelve la ruta relativa para usar en HTML.
    """
    logo_path = os.path.join(LOGO_DIR, f"{team_id}.png")
    logo_web_path = f"/static/img/logos/{team_id}.png"

    # Si ya existe, reutilizamos
    if os.path.exists(logo_path):
        return logo_web_path

    url = f"{BASE_URL}/teams/get-logo"
    params = {"teamId": team_id}

    try:
        r = requests.get(url, headers=HEADERS, params=params, stream=True, timeout=10)
        if r.status_code == 200:
            with open(logo_path, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            return logo_web_path
        else:
            print(f"Error {r.status_code} al descargar logo {team_id}")
            return "/static/img/logo_u.png"
    except Exception as e:
        print(f"Excepción descargando logo {team_id}: {e}")
        return "/static/img/logo_u.png"
