from app.config.db import devices_collection
from app.commands.handlers import dispatch_command
# from app.models.schema import validate_payload
from datetime import datetime, timezone
from bson import ObjectId


# converting MongoDB document to a JSON dict
def serialize_collection(device):
  return {
    "id": str(device["_id"]),
    "name": device["name"],
    "type": device["type"],
    "location": device.get("location"),
    "state": device.get("state"),
    "last_updated": device.get("last_update")
  }
  
  
# add a new device
def add_device(data):
  data["last_update"] = datetime.now(timezone.utc).isoformat()
  
  result = devices_collection.insert_one(data)
  new_device = devices_collection.find_one({"_id": result.inserted_id})
  return serialize_collection(new_device)


# display all device
def get_devices():
  devices = devices_collection.find()
  return [serialize_collection(device) for device in devices]


# display a device by id
def get_device(device_id):
  device = devices_collection.find_one({"_id": ObjectId(device_id)})
  return serialize_collection(device) if device else None


# Update device full details by ID
def get_device(device_id):
  device = devices_collection.find_one({"_id": ObjectId(device_id)})
  return serialize_collection(device) if device else None


# Update device full details by ID
def update(device_id, data):
  data["last_updated"] = datetime.now(timezone.utc).isoformat()
  
  result = devices_collection.update_one(
    {"_id": ObjectId(device_id)},
    {"$set": data}
  )
  
  if result.matched_count == 0:
    return None
  
  updated = devices_collection.find_one({"_id": ObjectId(device_id)})
  return serialize_collection(updated)


# partial update only
def patch(device_id, data):
  """
  Partially update a device's state or other fields without replacing entire state.
  This is intended for PATCH routes.
  """

  # Fetch existing device
  existing = devices_collection.find_one({"_id": ObjectId(device_id)})
  if not existing:
    return None

  # Merge nested "state" if provided
  if "state" in data:
    for key, value in data["state"].items():
      existing["state"][key] = value
    data["state"] = existing["state"]

  # Update timestamp
  data["last_updated"] = datetime.now(timezone.utc).isoformat()

  # Apply partial update to DB
  result = devices_collection.update_one(
    {"_id": ObjectId(device_id)},
    {"$set": data}
  )

  if result.matched_count == 0:
    return None

  updated = devices_collection.find_one({"_id": ObjectId(device_id)})
  return serialize_collection(updated)


# delete device by ID
def delete_device(device_id):
  device = devices_collection.delete_one({"_id": ObjectId(device_id)})
  return device.deleted_count > 0


def send_command_to_device(device_id, command):
  device = get_device(device_id)
  
  if not device:
    return None
  
  # dispatch command to the correct handler
  result = dispatch_command(device, command)
  
  if "error" in result:
    return result
  
  # update DB after command
  update(device_id, {"state": result["updated_state"]})
  
  return result
