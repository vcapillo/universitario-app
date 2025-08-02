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


def get_team_fixtures(team_id: int = TEAM_ID, page_index: int = 0, limit: int = 5):
    """
    Obtiene los próximos partidos del equipo.
    Solo retorna los próximos `limit` (por defecto 5).
    """
    url = f"{BASE_URL}/teams/get-next-matches"
    params = {"teamId": team_id, "pageIndex": page_index}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    data = r.json()

    events = data.get("events", [])

    # Nos quedamos solo con los próximos N
    events = events[:limit]

    # Agregamos logos a los equipos
    for match in events:
        try:
            match["homeTeam"]["logo"] = get_team_logo(match["homeTeam"]["id"])
            match["awayTeam"]["logo"] = get_team_logo(match["awayTeam"]["id"])
        except Exception as e:
            print(f"Error cargando logo: {e}")
            match["homeTeam"]["logo"] = "/static/img/logo_u.png"
            match["awayTeam"]["logo"] = "/static/img/logo_u.png"

    return events



def get_standings(tournament_id: int = TOURNAMENT_ID, season_id: int = SEASON_ID):
    """
    Obtiene la tabla de posiciones de la Liga 1 Clausura 2025.
    Marca los equipos que están jugando actualmente.
    """
    url = f"{BASE_URL}/tournaments/get-standings"
    params = {"tournamentId": tournament_id, "seasonId": season_id, "type": "total"}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    data = r.json()

    rows = data.get("standings", [])[0].get("rows", [])

    # Obtener todos los partidos en vivo
    live_matches = get_live_matches()
    live_teams = {match["homeTeam"]["id"] for match in live_matches} | {match["awayTeam"]["id"] for match in live_matches}

    # Agregar logos y flag de "jugando"
    for row in rows:
        try:
            row["team"]["logo"] = get_team_logo(row["team"]["id"])
        except Exception:
            row["team"]["logo"] = "/static/img/logo_u.png"

        row["team"]["isPlaying"] = row["team"]["id"] in live_teams

    return rows






def get_team_past_matches(team_id: int = TEAM_ID, page_index: int = 0, limit: int = 6):
    """
    Obtiene los últimos partidos jugados por el equipo.
    Retorna los más recientes primero, limitados a 'limit'.
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

    # Ordenar por fecha descendente (más recientes primero)
    events_sorted = sorted(events, key=lambda x: x.get("startTimestamp", 0), reverse=True)

    # Devolver solo los últimos 'limit'
    return events_sorted[:limit]





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

def get_live_matches():
    """
    Retorna todos los eventos de fútbol en vivo.
    """
    url = f"{BASE_URL}/tournaments/get-live-events"
    params = {"sport": "football"}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json().get("events", [])
