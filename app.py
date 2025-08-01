from flask import Flask, render_template
from sofascore_api import get_team_fixtures, get_standings, get_team_logo
import datetime

app = Flask(__name__)

# -------------------------------
# Filtro para formatear fechas
# -------------------------------
@app.template_filter("datetimeformat")
def datetimeformat(value, format="%d/%m/%Y %H:%M"):
    """Convierte timestamps en fecha legible"""
    try:
        return datetime.datetime.fromtimestamp(value).strftime(format)
    except Exception:
        return value

# -------------------------------
# Rutas principales
# -------------------------------
@app.route("/")
def index():
    """Página principal con portada"""
    return render_template("home.html", active_page="home")


@app.route("/fixtures")
def fixtures():
    """Calendario de partidos de Universitario"""
    try:
        data = get_team_fixtures()
        matches = data.get("events", [])
        # Agregamos los logos de cada equipo
        for match in matches:
            match["homeLogo"] = get_team_logo(match["homeTeam"]["id"])
            match["awayLogo"] = get_team_logo(match["awayTeam"]["id"])
    except Exception as e:
        matches = []
        print(f"Error cargando fixtures: {e}")

    return render_template("fixtures.html", fixtures=matches, active_page="fixtures")


@app.route("/standings")
def standings():
    """Tabla de posiciones del Clausura"""
    try:
        data = get_standings()
        standings = data.get("standings", [])[0].get("rows", [])
        # Agregamos el logo de cada equipo
        for row in standings:
            row["team"]["logo"] = get_team_logo(row["team"]["id"])
    except Exception as e:
        standings = []
        print(f"Error cargando standings: {e}")

    return render_template("standings.html", standings=standings, active_page="standings")


# -------------------------------
# Render (Gunicorn)
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
