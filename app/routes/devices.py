# Blueprints for Home devices
from flask import Blueprint, request, jsonify
from app.services.service import add_device, get_devices, get_device, update, delete_device
from app.models.schema import device_schema, patch_schema, validate_request

device_bp = Blueprint("devices", __name__)


@device_bp.route("", methods=["GET"])
def list_devices():
  return jsonify(get_devices())


@device_bp.route("new/", methods=["POST"])
def new_device():
  data = request.json
  
  validated = validate_request(device_schema, data)
  if "errors" in validated:
    return jsonify(validated), 400   # Bad Request
  
  device = add_device(validated)
  return jsonify({"message": "Device created", "data": device}), 200


@device_bp.route("<device_id>/", methods=["GET"])
def list_device(device_id):
  device = get_device(device_id)
  if not device:
    return jsonify({"error": "Device not found"}), 404
  return jsonify(device)


@device_bp.route("update/<device_id>/", methods=["PUT"])
def update_device(device_id):
  data = request.json
  validated = validate_request(device_schema, data)
  if "errors" in validated:
    return jsonify(validated), 400
  
  updated = update(device_id, validated)
  
  if not updated:
    return jsonify({"error": "Device not found"}), 404
  
  return jsonify({"message": "Device update", "data": updated})


@device_bp.route("patch/<device_id>/", methods=["PATCH"])
def partial_update(device_id):
  data = request.json
  
  # allow any subfield of a device
  validated = validate_request(patch_schema, data)
  if "errors" in validated:
    return jsonify(validated), 400
  
  updated = update(device_id, validated)
  if not updated:
    return jsonify({"error": "Device not found"}), 404
  
  return jsonify({"message": "Device patched", "data": updated})


@device_bp.route("del/<device_id>/", methods=["DELETE"])
def delete(device_id):
  deleted= delete_device(device_id)
  
  if not deleted:
    return jsonify({"error": "Device not found"}), 404
  return jsonify({"message": "Device deleted"})
