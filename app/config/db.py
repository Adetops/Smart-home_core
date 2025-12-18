import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
cluster = os.getenv("MONGODB_CLUSTER")
db_name = os.getenv("MONGODB_DB")

if not all([username, password, cluster, db_name]):
    raise RuntimeError("MongoDB environment variables are not set")

uri = (
    f"mongodb+srv://{username}:{password}@{cluster}/"
    f"{db_name}?retryWrites=true&w=majority"
)

client = MongoClient(uri, server_api=ServerApi("1"))

try:
    client.admin.command("ping")
    print("MongoDB connected successfully")
except Exception as e:
    raise RuntimeError(f"MongoDB connection failed: {e}")
