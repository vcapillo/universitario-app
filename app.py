from flask import Flask, jsonify
import sofascore_api

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>¡Y dale U!</h1><p>Seguimiento del Clausura 2025</p>"

@app.route("/fixtures")
def fixtures():
    data = sofascore_api.get_team_fixtures()
    return jsonify(data)

@app.route("/tabla")
def tabla():
    data = sofascore_api.get_standings()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)