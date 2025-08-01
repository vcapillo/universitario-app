from flask import Flask, render_template
from sofascore_api import get_team_fixtures, get_team_past_matches ,get_standings, get_team_logo
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
    try:
        next_matches = get_team_fixtures()
        past_matches = get_team_past_matches()
    except Exception as e:
        next_matches, past_matches = [], []
    return render_template(
        "fixtures.html",
        next_matches=next_matches,
        past_matches=past_matches,
        active_page="fixtures"
    )




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
