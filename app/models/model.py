from datetime import datetime, timezone


def user_schema(user):
  """
  Convert MongoDB user document to JSON-safe format.
  NEVER return password hashes.
  """
  return {
    "id": str(user["_id"]),
    "username": user["username"],
    "role": user.get("role", "user"),
    "created_at": user.get("created_at")
  }


def new_user(username, password_hash, role="user"):
  """
  Create a new user document.
  """
  return {
    "username": username,
    "password": password_hash,
    "role": role,
    "created_at": datetime.now(timezone.utc).isoformat()
  }



class Device:
  def __init__(self, device_id, name, type, location, state):
    self.id = device_id
    self.name = name
    self.type = type
    self.location = location
    self.state = state
    self.last_updated = None
  
  def to_dict(self):
    return {
			"id": self.id,
			"name": self.name,
			"type": self.type,
			"location": self.location,
			"state": self.state,
			"last_updated": self.last_updated
		}
