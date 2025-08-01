from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>¡Y dale U!</h1><p>App de Universitario en Flask corriendo en Codespaces</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)