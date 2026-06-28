import pandas as pd

from pymongo import MongoClient

from config import config

client = MongoClient(config.MONGO_URI)

db = client[config.DB_NAME]

df = pd.read_csv("data/movies.csv")

movies = df.to_dict(orient="records")

db.movies.insert_many(movies)

print("Movies imported successfully 🔥")