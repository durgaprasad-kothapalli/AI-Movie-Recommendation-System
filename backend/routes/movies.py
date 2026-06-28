from flask import Blueprint, request, jsonify
from ml.recommender import Recommender

movies_bp = Blueprint("movies", __name__)

def _serialise(m: dict):

    return {
        "movieId": int(m.get("movieId", 0)),
        "title": str(m.get("title", "")),
        "genres": str(m.get("genres", "")),
        "description": str(m.get("description", "")),
        "poster_url": str(m.get("poster_url", "")),
        "release_year": str(m.get("release_year", "N/A")),
    }

@movies_bp.route("/movies", methods=["GET"])
def get_movies():
    rec    = Recommender.get_instance()
    query  = request.args.get("q", "").strip()
    genre  = request.args.get("genre", "").strip()
    page   = max(int(request.args.get("page", 1)), 1)
    limit  = min(int(request.args.get("limit", 20)), 100)

    movies = rec.search_movies(query) if query else rec.get_all_movies()

    if genre:
        movies = [m for m in movies if genre.lower() in str(m.get("genres", "")).lower()]

    total  = len(movies)
    start  = (page - 1) * limit
    paged  = movies[start: start + limit]

    return jsonify({"movies": [_serialise(m) for m in paged], "total": total, "page": page}), 200

@movies_bp.route("/movie/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    rec = Recommender.get_instance()
    m   = rec.get_movie(movie_id)
    if not m:
        return jsonify({"error": "Movie not found."}), 404
    return jsonify(_serialise(m)), 200

@movies_bp.route("/movies/search", methods=["GET"])
def search_movies():
    q   = request.args.get("q", "").strip()
    rec = Recommender.get_instance()
    results = rec.search_movies(q) if q else []
    return jsonify({"results": [_serialise(m) for m in results[:10]]}), 200

@movies_bp.route("/movies/genres", methods=["GET"])
def get_genres():
    rec    = Recommender.get_instance()
    movies = rec.get_all_movies()
    genres = set()
    for m in movies:
        for g in str(m.get("genres", "")).split("|"):
            if g.strip():
                genres.add(g.strip())
    return jsonify({"genres": sorted(genres)}), 200
