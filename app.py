from flask import Flask, jsonify
import sofascore_api

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>¡Y dale U!</h1><p>Seguimiento Clausura 2025</p>"

# Ruta JSON con fixtures de Universitario
@app.route("/api/fixtures")
def fixtures():
    data = sofascore_api.get_team_fixtures()
    return jsonify(data)

# Ruta JSON con tabla Clausura 2025
@app.route("/api/standings")
def standings():
    data = sofascore_api.get_standings()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
