import datetime
import jwt
import bcrypt

from flask import Blueprint, request, jsonify
from pymongo import MongoClient

from config import config

auth_bp = Blueprint("auth", __name__)
client  = MongoClient(config.MONGO_URI)
db      = client[config.DB_NAME]

def _make_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=config.JWT_EXPIRY_HOURS),
    }
    return jwt.encode(payload, config.JWT_SECRET, algorithm="HS256")

def verify_token(token: str):
    try:
        return jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required."}), 400
    if db.users.find_one({"email": email}):
        return jsonify({"error": "Email already registered."}), 409

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    result = db.users.insert_one({
        "username": username,
        "email":    email,
        "password": hashed,
        "created_at": datetime.datetime.utcnow(),
        "recently_viewed": [],
    })
    user_id = str(result.inserted_id)
    return jsonify({"message": "Registered successfully.", "token": _make_token(user_id),
                    "user": {"user_id": user_id, "username": username, "email": email}}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data  = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = db.users.find_one({"email": email})
    if not user or not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return jsonify({"error": "Invalid email or password."}), 401

    user_id = str(user["_id"])
    return jsonify({
        "token": _make_token(user_id),
        "user":  {"user_id": user_id, "username": user["username"], "email": user["email"]},
    }), 200


@auth_bp.route("/google-login", methods=["POST"])
def google_login():

    data = request.get_json()

    email = data.get("email")
    name = data.get("name")
    picture = data.get("picture")

    if not email:
        return jsonify({
            "error": "Email required"
        }), 400

    existing_user = db.users.find_one({
        "email": email
    })

    if not existing_user:

        db.users.insert_one({
            "username": name,
            "email": email,
            "picture": picture
        })

    token = jwt.encode(
        {
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
        },
        config.JWT_SECRET,
        algorithm="HS256"
    )

    return jsonify({
        "token": token,
        "user": {
            "email": email,
            "username": name,
            "picture": picture
        }
    })