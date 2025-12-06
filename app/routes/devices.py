# Blueprints for Home devices
from flask import Blueprint, request, jsonify

devices_bp = Blueprint('devices', __name__, url_prefix='/devices')

DEVICES = [
	{"id": 1, "name": "Living Room Light", "type": "light", "state": {"on": False}},
	{"id": 2, "name": "Front Door Lock", "type": "lock", "state": {"locked": True}}
]

@devices_bp.route("/", methods=["GET",])
def devices_list():
  return jsonify(DEVICES)

@devices_bp.route("/<int:device_id>", methods=["GET"])
def get_device(device_id):
  for device in DEVICES:
    if device["id"] == device_id:
      return jsonify(device)
  return jsonify({"error": "Device not found"}), 404

@devices_bp.route("/new/", methods=["POST"])
def add_device():
  content = request.json
  DEVICES.append(content)
  return jsonify({"message": "New device added", "data": content})
