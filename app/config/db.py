import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# MongoDB connection URI (env-first, fallback to local)
MONGO_URI = os.getenv(
  "MONGO_URI",
  "mongodb://localhost:27017/home_automation"
)

# Create client with timeout (prevents app hanging forever)
client = MongoClient(
  MONGO_URI,
  serverSelectionTimeoutMS=5000
)

try:
  # Force connection check at startup
  client.admin.command("ping")
except ServerSelectionTimeoutError as e:
  raise RuntimeError(f"MongoDB connection failed: {e}")

# Get database from URI
db = client.get_default_database()

# Collections
devices_collection = db["devices"]
