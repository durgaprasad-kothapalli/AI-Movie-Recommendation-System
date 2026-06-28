import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class CollaborativeRecommender:
    def __init__(self):
        self.user_movie_matrix = None
        self.user_sim_df       = None
        self.movies_df         = None

    def fit(self, ratings_df: pd.DataFrame, movies_df: pd.DataFrame):
        self.movies_df = movies_df.copy()
        self.user_movie_matrix = ratings_df.pivot_table(
            index="userId", columns="movieId", values="rating"
        ).fillna(0)
        sim = cosine_similarity(self.user_movie_matrix)
        self.user_sim_df = pd.DataFrame(
            sim,
            index=self.user_movie_matrix.index,
            columns=self.user_movie_matrix.index,
        )
        return self

    def recommend(self, user_id: int, top_n: int = 10):
        if self.user_sim_df is None or user_id not in self.user_sim_df.index:
            # Cold-start: return top-rated movies overall
            return self._popular_fallback(top_n)

        similar_users = (
            self.user_sim_df[user_id]
            .sort_values(ascending=False)
            .drop(index=user_id, errors="ignore")
            .head(5)
            .index.tolist()
        )
        already_seen = set(
            self.user_movie_matrix.loc[user_id][
                self.user_movie_matrix.loc[user_id] > 0
            ].index.tolist()
        )
        scores = {}
        for su in similar_users:
            row = self.user_movie_matrix.loc[su]
            weight = self.user_sim_df.loc[user_id, su]
            for mid, rating in row[row > 0].items():
                if mid not in already_seen:
                    scores[mid] = scores.get(mid, 0) + rating * weight

        sorted_ids = sorted(scores, key=scores.get, reverse=True)[:top_n]
        return self._build_result(sorted_ids, scores)

    def _popular_fallback(self, top_n: int):
        col_means = self.user_movie_matrix.replace(0, pd.NA).mean()
        top_ids = col_means.sort_values(ascending=False).head(top_n).index.tolist()
        return self._build_result(top_ids, col_means.to_dict())

    def _build_result(self, movie_ids, scores):
        results = []
        for mid in movie_ids:
            row = self.movies_df[self.movies_df["movieId"] == mid]
            if row.empty:
                continue
            m = row.iloc[0]
            results.append({
                "movieId":    int(m["movieId"]),
                "title":      m["title"],
                "genres":     m["genres"],
                "poster_url": m.get("poster_url", ""),
                "score":      round(float(scores.get(mid, 0)), 4),
            })
        return results
