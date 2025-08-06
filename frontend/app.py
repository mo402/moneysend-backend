from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="frontend")
CORS(app)

@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data["username"] == "admin" and data["password"] == "admin":
        return jsonify({"token": "vrai-token"})
    return jsonify({"message": "Identifiants invalides"}), 401

@app.route("/send-money", methods=["POST"])
def send_money():
    auth = request.headers.get("Authorization", "")
    if "vrai-token" not in auth:
        return jsonify({"message": "Non autorisé"}), 403
    return jsonify({"message": "Transfert réussi !"})

if __name__ == "__main__":
    app.run(debug=True)
