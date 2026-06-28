"""
recommender.py
Central facade: loads data, trains models, exposes recommend().
"""

from .data_loader import load_movies, load_ratings
from .content_based import ContentBasedRecommender
from .collaborative import CollaborativeRecommender
from .hybrid import HybridRecommender


class Recommender:

    _instance = None

    def __init__(self):

        movies_df = load_movies()
        ratings_df = load_ratings()

        self.movies_df = movies_df

        print(self.movies_df.head())

        self.cb = ContentBasedRecommender().fit(movies_df)

        self.cf = CollaborativeRecommender().fit(
            ratings_df,
            movies_df
        )

        self.hybrid = HybridRecommender(
            self.cb,
            self.cf
        )

    # ─────────────────────────────────────────────

    @classmethod
    def get_instance(cls):

        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    # ─────────────────────────────────────────────

    def recommend(
        self,
        movie_id: int,
        user_id: int = None,
        method: str = "hybrid",
        top_n: int = 10
    ):

        print("MOVIE ID:", movie_id)
        print("METHOD:", method)

        if method == "content":

            result = self.cb.recommend(
                movie_id,
                top_n
            )

            print(result)

            return result

        if method == "collaborative":

            result = self.cf.recommend(
                user_id,
                top_n
            )

            print(result)

            return result

        result = self.hybrid.recommend(
            movie_id,
            user_id,
            top_n
        )

        print(result)

        return result

    # ─────────────────────────────────────────────

    def get_all_movies(self):

        return self.movies_df.to_dict(
            orient="records"
        )

    # ─────────────────────────────────────────────

    def get_movie(self, movie_id: int):

        row = self.movies_df[
            self.movies_df["movieId"] == movie_id
        ]

        if not row.empty:
            return row.iloc[0].to_dict()

        return None

    # ─────────────────────────────────────────────

    def search_movies(self, query: str):

        q = query.lower()

        mask = self.movies_df["title"] \
            .str.lower() \
            .str.contains(q, na=False)

        return self.movies_df[mask] \
            .to_dict(orient="records")