from pymongo import MongoClient


# Connect to the local MongoDb instance
client = MongoClient("mongodb://localhost:27017/")

# select [or create] the database
db = client["home_automation"]

# select [or create] the collection
devices_collection = db["devices"]
