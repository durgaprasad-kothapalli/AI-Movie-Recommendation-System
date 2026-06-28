from flask import Blueprint, request, jsonify

from ml.recommender import Recommender

recommend_bp = Blueprint(
    "recommend",
    __name__
)

# ─────────────────────────────────────────

@recommend_bp.route(
    "/recommend/<int:movie_id>",
    methods=["GET"]
)

def recommend(movie_id):

    method = request.args.get(
        "method",
        "content"
    )

    top_n = min(
        int(request.args.get("top_n", 10)),
        30
    )

    user_id = request.args.get(
        "user_id"
    )

    try:

        if user_id:
            user_id = int(user_id)

    except:
        user_id = None

    rec = Recommender.get_instance()

    results = rec.recommend(
        movie_id=movie_id,
        user_id=user_id,
        method=method,
        top_n=top_n
    )

    return jsonify({

        "movie_id": movie_id,

        "method": method,

        "recommendations": results

    }), 200