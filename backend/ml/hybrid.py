class HybridRecommender:
    """Merges Content-Based and Collaborative results using weighted rank scoring."""

    def __init__(self, cb_model, cf_model, cb_weight=0.5, cf_weight=0.5):
        self.cb  = cb_model
        self.cf  = cf_model
        self.cb_w = cb_weight
        self.cf_w = cf_weight

    def recommend(self, movie_id: int, user_id: int = None, top_n: int = 10):
        cb_results = self.cb.recommend(movie_id, top_n=top_n * 2)
        cf_results = self.cf.recommend(user_id, top_n=top_n * 2) if user_id else []

        scores = {}
        meta   = {}

        for rank, item in enumerate(cb_results):
            mid = item["movieId"]
            scores[mid] = scores.get(mid, 0) + self.cb_w * (1 / (rank + 1))
            meta[mid]   = item

        for rank, item in enumerate(cf_results):
            mid = item["movieId"]
            scores[mid] = scores.get(mid, 0) + self.cf_w * (1 / (rank + 1))
            if mid not in meta:
                meta[mid] = item

        # Remove the queried movie itself
        scores.pop(movie_id, None)
        meta.pop(movie_id, None)

        ranked = sorted(scores, key=scores.get, reverse=True)[:top_n]
        results = []
        for mid in ranked:
            entry = meta[mid].copy()
            entry["score"] = round(scores[mid], 4)
            results.append(entry)
        return results
