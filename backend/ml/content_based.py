import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedRecommender:

    def __init__(self):

        self.cosine_sim = None
        self.indices = None
        self.movies_df = None

    # ─────────────────────────────────────────

    def fit(self, movies_df: pd.DataFrame):

        self.movies_df = movies_df.copy().reset_index(drop=True)

        # Build feature string

        self.movies_df["features"] = (

            self.movies_df["genres"]
            .fillna("")
            .str.replace("|", " ", regex=False)

            + " " +

            self.movies_df.get(
                "description",
                pd.Series([""] * len(self.movies_df))
            ).fillna("")
        )

        tfidf = TfidfVectorizer(
            stop_words="english"
        )

        matrix = tfidf.fit_transform(
            self.movies_df["features"]
        )

        self.cosine_sim = cosine_similarity(
            matrix,
            matrix
        )

        self.indices = pd.Series(
            self.movies_df.index,
            index=self.movies_df["title"].str.lower()
        ).drop_duplicates()

        return self

    # ─────────────────────────────────────────

    def recommend(
        self,
        movie_id: int,
        top_n: int = 10
    ):

        if self.movies_df is None:
            return []

        row = self.movies_df[
            self.movies_df["movieId"]
            .astype(int) == int(movie_id)
        ]

        if row.empty:
            return []

        idx = row.index[0]

        sim_scores = list(
            enumerate(self.cosine_sim[idx])
        )

        sim_scores = sorted(
            sim_scores,
            key=lambda x: x[1],
            reverse=True
        )

        sim_scores = [
            s for s in sim_scores
            if s[0] != idx
        ][:top_n]

        results = []

        for i, score in sim_scores:

            m = self.movies_df.iloc[i]

            results.append({

                "movieId": int(m["movieId"]),

                "title": str(m["title"]),

                "genres": str(m["genres"]),

                "poster_url": str(
                    m.get("poster_url", "")
                ),

                "score": round(
                    float(score),
                    4
                )
            })

        return results