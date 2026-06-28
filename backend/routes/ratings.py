import datetime
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from routes.auth import verify_token
from config import config

ratings_bp = Blueprint("ratings", __name__)
client = MongoClient(config.MONGO_URI)
db     = client[config.DB_NAME]

def _get_user(req):
    token = req.headers.get("Authorization", "").replace("Bearer ", "").strip()
    return verify_token(token)

@ratings_bp.route("/rate", methods=["POST"])
def rate():

    data = request.get_json(silent=True) or {}

    user = data.get("user")
    movie_id = data.get("movie_id")
    rating = data.get("rating")

    if user is None or movie_id is None or rating is None:
        return jsonify({
            "error": "user, movie_id and rating are required."
        }), 400

    if not (0.5 <= float(rating) <= 5.0):
        return jsonify({
            "error": "Rating must be between 0.5 and 5.0."
        }), 400

    db.ratings.update_one(
        {
            "user": user,
            "movie_id": int(movie_id)
        },
        {
            "$set": {
                "rating": float(rating),
                "timestamp": datetime.datetime.utcnow()
            }
        },
        upsert=True,
    )

    return jsonify({
        "message": "Rating saved."
    }), 200

@ratings_bp.route("/ratings/<int:movie_id>", methods=["GET"])
def get_ratings(movie_id):
    docs = list(db.ratings.find({"movie_id": movie_id}, {"_id": 0}))
    avg  = sum(d["rating"] for d in docs) / len(docs) if docs else 0
    return jsonify({"movie_id": movie_id, "average": round(avg, 2),
                    "count": len(docs)}), 200

@ratings_bp.route("/ratings/user", methods=["GET"])
def user_ratings():
    payload = _get_user(request)
    if not payload:
        return jsonify({"error": "Unauthorised."}), 401
    docs = list(db.ratings.find({"user_id": payload["user_id"]}, {"_id": 0}))
    return jsonify({"ratings": docs}), 200
