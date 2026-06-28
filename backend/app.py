from flask import Flask, request, jsonify
from flask_cors import CORS

from routes.auth      import auth_bp
from routes.movies    import movies_bp
from routes.recommend import recommend_bp
from routes.ratings   import ratings_bp
from routes.watchlist import watchlist_bp
from config           import config

watchlists = {}
def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(auth_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(recommend_bp)
    app.register_blueprint(ratings_bp)
    app.register_blueprint(watchlist_bp)

    # Pre-load ML models at startup
    from ml.recommender import Recommender
    Recommender.get_instance()
    print("✅ ML models loaded.")



    @app.route('/watchlist/add', methods=['POST'])
    def add_watchlist():

        data = request.json

        user = data.get('user')
        movie = data.get('movie')

        if user not in watchlists:
            watchlists[user] = []

        watchlists[user].append(movie)

        return jsonify({
            "message": "Movie added to watchlist"
        })


    @app.route('/watchlist/<user>')
    def get_watchlist(user):

        movies = watchlists.get(user, [])

        return jsonify({
            "watchlist": movies
        })
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=config.FLASK_PORT)


