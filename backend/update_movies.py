import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from urllib.parse import quote
import requests

from pymongo import MongoClient
from config import config

TMDB_API_KEY = "eeff4fdb9f4155e1267ac69f579453cd"

client = MongoClient(config.MONGO_URI)

db = client[config.DB_NAME]

movies_collection = db.movies

movies = list(movies_collection.find())

for movie in movies:

    title = movie.get("title", "")

    clean_title = title.split("(")[0].strip()
    encoded_title = quote(clean_title)

    url = (
        f"https://api.themoviedb.org/3/search/movie"
        f"?api_key={TMDB_API_KEY}"
        f"&query={encoded_title}"
    )

    try:

        response = requests.get(
             url,
             timeout=None,
             verify=False
)

        data = response.json()

        results = data.get("results")

        if results:

            tmdb_movie = results[0]

            movies_collection.update_one(
                {"_id": movie["_id"]},
                {
                    "$set": {
                        "poster_path": tmdb_movie.get("poster_path"),
                        "overview": tmdb_movie.get("overview"),
                        "backdrop_path": tmdb_movie.get("backdrop_path")
                    }
                }
            )

            print(f"✅ Updated: {title}")

        else:

            print(f"❌ No result: {title}")

    except Exception as e:

        print(f"❌ Error for {title}: {e}")

print("🔥 DONE")