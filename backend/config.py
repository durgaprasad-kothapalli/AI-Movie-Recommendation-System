import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI      = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME        = os.getenv("DB_NAME", "movie_recommendation_db")
    JWT_SECRET     = os.getenv("JWT_SECRET", "dev_secret_change_me")
    JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", 24))
    FLASK_PORT     = int(os.getenv("FLASK_PORT", 5000))

config = Config()
