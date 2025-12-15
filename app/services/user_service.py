from app.config.db import db
from app.models.model import new_user, user_schema
from app.utils.password import hash_password, verify_password


users_collection = db["users"]


def create_user(username, password, role="user"):
  if users_collection.find_one({"username": username}):
    return None
  
  user = new_user(username, hash_password(password), role)
  result = users_collection.insert_one(user)
  user["_id"] = result.inserted_id
  return user_schema(user)


def authenticate_user(username, password):
  user = users_collection.find_one({"username": username})
  if not user:
    return None
  
  if not verify_password(password, user["password"]):
    return None
  
  return user
