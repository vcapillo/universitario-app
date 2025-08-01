from flask import Flask, render_template
from sofascore_api import get_team_fixtures, get_standings

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", active_page="home")

@app.route("/fixtures")
def fixtures():
    data = get_team_fixtures()
    return render_template("fixtures.html", fixtures=data, active_page="fixtures")

@app.route("/standings")
def standings():
    data = get_standings()
    return render_template("standings.html", standings=data, active_page="standings")

if __name__ == "__main__":
    app.run(debug=True)
