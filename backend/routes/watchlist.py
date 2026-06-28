import datetime
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from routes.auth import verify_token
from ml.recommender import Recommender
from config import config

watchlist_bp = Blueprint("watchlist", __name__)
client = MongoClient(config.MONGO_URI)
db     = client[config.DB_NAME]

def _get_user(req):
    token = req.headers.get("Authorization", "").replace("Bearer ", "").strip()
    return verify_token(token)

@watchlist_bp.route("/watchlist", methods=["POST"])
def add_to_watchlist():
    payload = _get_user(request)
    if not payload:
        return jsonify({"error": "Unauthorised."}), 401

    data     = request.get_json(silent=True) or {}
    movie_id = data.get("movie_id")
    if movie_id is None:
        return jsonify({"error": "movie_id is required."}), 400

    exists = db.watchlist.find_one(
        {"user_id": payload["user_id"], "movie_id": int(movie_id)}
    )
    if exists:
        return jsonify({"message": "Already in watchlist."}), 200

    db.watchlist.insert_one({
        "user_id":  payload["user_id"],
        "movie_id": int(movie_id),
        "added_at": datetime.datetime.utcnow(),
    })
    return jsonify({"message": "Added to watchlist."}), 201

@watchlist_bp.route("/watchlist", methods=["GET"])
def get_watchlist():
    payload = _get_user(request)
    if not payload:
        return jsonify({"error": "Unauthorised."}), 401

    rec   = Recommender.get_instance()
    docs  = list(db.watchlist.find({"user_id": payload["user_id"]}, {"_id": 0}))
    items = []
    for d in docs:
        m = rec.get_movie(d["movie_id"])
        if m:
            items.append({
                "movie_id":   int(m["movieId"]),
                "title":      str(m["title"]),
                "poster_url": str(m.get("poster_url", "")),
                "genres":     str(m.get("genres", "")),
                "added_at":   str(d.get("added_at", "")),
            })
    return jsonify({"watchlist": items}), 200

@watchlist_bp.route("/watchlist/<int:movie_id>", methods=["DELETE"])
def remove_from_watchlist(movie_id):
    payload = _get_user(request)
    if not payload:
        return jsonify({"error": "Unauthorised."}), 401
    db.watchlist.delete_one({"user_id": payload["user_id"], "movie_id": movie_id})
    return jsonify({"message": "Removed from watchlist."}), 200
