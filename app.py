from flask import Flask, render_template
from sofascore_api import get_team_fixtures, get_standings
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
    return render_template("base.html", active_page="home")

@app.route("/fixtures")
def fixtures():
    try:
        data = get_team_fixtures()
    except Exception as e:
        data = {"error": str(e)}
    return render_template("fixtures.html", fixtures=data, active_page="fixtures")

@app.route("/standings")
def standings():
    try:
        data = get_standings()
    except Exception as e:
        data = {"error": str(e)}
    return render_template("standings.html", standings=data, active_page="standings")

# -------------------------------
# Render (Gunicorn)
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
