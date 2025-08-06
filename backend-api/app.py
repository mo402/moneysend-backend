from flask import Flask, send_from_directory, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import hashlib
import jwt
import datetime

app = Flask(__name__)
CORS(app)

# === Config ===
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'votre_clef_super_secrete'
db = SQLAlchemy(app)

# === Models ===
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# === Créer la BDD si pas encore ===
with app.app_context():
    db.create_all()

# === Routes API ===
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = hashlib.sha256(data.get('password').encode()).hexdigest()

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Utilisateur existe déjà'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Utilisateur enregistré'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = hashlib.sha256(data.get('password').encode()).hexdigest()
    user = User.query.filter_by(username=username, password=password).first()

    if user:
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Identifiants invalides'}), 401

# === Routes statiques ===

# Frontend index.html
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

# Fichiers frontend (CSS, JS si ajoutés plus tard)
@app.route('/<path:path>')
def frontend_files(path):
    return send_from_directory('frontend', path)

# Fichiers PWA (sw.js, manifest.json, icons)
@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

# === Lancer serveur ===
if __name__ == '__main__':
    app.run(debug=True)
