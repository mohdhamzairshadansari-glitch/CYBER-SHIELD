import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
MONGO_DATABASE = os.getenv("MONGO_DATABASE")

client = MongoClient(
    f"mongodb://{MONGO_HOST}:{MONGO_PORT}"
)

db = client[MONGO_DATABASE]

raw_events = db["raw_events"]