# Blueprints for Home devices
from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from .validation import validate_device_data

devices_bp = Blueprint('devices', __name__, url_prefix='/devices/')

DEVICES = []
required_fields = ["id", "name", "type", "location", "state"]

def current_timestamp():
  return datetime.now(timezone.utc).isoformat()

# Get all devices 
@devices_bp.route("", methods=["GET"])
def devices_list():
  return jsonify(DEVICES)

# Get a device by its ID
@devices_bp.route("<int:device_id>/", methods=["GET"])
def get_device(device_id):
  for device in DEVICES:
    if device["id"] == device_id:
      return jsonify(device)
  return jsonify({"error": "Device not found"}), 404

# Add a new device to my list
@devices_bp.route("new/", methods=["POST"])
def add_device():
  content = request.json
  
  # validate the required fields
  # for field in required_fields:
  #   if field not in content:
  #     return jsonify({"error": f"Missing field: {field}"}), 400
  
  errors = validate_device_data(content, required=True)
  if errors:
    return jsonify({"errors": errors}), 400
  
  # append the new device to my devices list
  DEVICES.append(content)
    
  # update the timestamp
  content["last_updated"] = current_timestamp()
  
  return jsonify({"message": "New device added", "data": content}), 201

# To update the status of any device given its ID
@devices_bp.route("update/<int:device_id>/", methods=["PUT"])
def update_device(device_id):
  content = request.json
  errors = validate_device_data(content, required=False)
  if errors:
    return jsonify({"errors": errors}), 400
  
  for device in DEVICES:
    if device["id"] == device_id:
      # if "state" in content:
      #   device["state"] = content["state"]
      for field in ["name", "type", "state", "location"]:
        if field in content:
          device[field] = content[field]
          
      device["last_updated"] = current_timestamp()
      return jsonify({"message": f'Device {device["name"]} successfully updated', "data": device})
  return jsonify({"error": "Device not found"}), 404

# To remove a device from my list by ID
@devices_bp.route("del/<int:device_id>/", methods=["DELETE"])
def delete_device(device_id):
  for device in DEVICES:
    if device["id"] == device_id:
      DEVICES.remove(device)
      return jsonify({"message": f'{device["name"]} is now deleted', "data": device})
  return jsonify({"error": "Device not found"}), 404

# For a partial update
@devices_bp.route("patch/<int:device_id>/", methods=["PATCH"])
def partial_update(device_id):
  content = request.json
  errors = validate_device_data(content, required=False)
  if errors:
    return jsonify({"errors": errors}), 400
  
  for device in DEVICES:
    if device["id"] == device_id:
      if "remove" in content:
        for field in content["remove"]:
          if field in device:
            del device[field]

      for key, value in content.items():
        if key == "state":
          device["state"].update(value)
        elif key != "remove":
          device[key] = value

      device["last_updated"] = current_timestamp()
      return jsonify({"message": f'{device["name"]} succesfully updated!', "data": device})
  return jsonify({"error": "Device not found"}), 404
