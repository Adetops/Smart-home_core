# Blueprints for Home devices
from flask import Blueprint, request, jsonify
import app
from app.services.device_service import add_device, get_devices, send_command_to_device, get_device, update, delete_device, patch
from app.models.schema import device_schema, patch_schema, validate_request
from app.utils.auth import require_api_key
from app.utils.roles import require_role
from app.utils.audit import log_audit_event
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging



device_bp = Blueprint("devices", __name__)


@device_bp.route("/", methods=["GET"])
def list_devices():
  return jsonify(get_devices())


@device_bp.route("/new", methods=["POST"])
@jwt_required()
@require_role("admin")
def new_device():
  data = request.json
  
  validated = validate_request(device_schema, data)
  if "errors" in validated:
    return jsonify(validated), 400   # Bad Request
  
  device = add_device(validated)
  
  app.socketio.emit("device_created", device)
  
  logging.info("Device created: %s", device["name"])

  log_audit_event(
    user=get_jwt_identity(),
    action="CREATE_DEVICE",
    resource=device["id"],
    details=device
  )
  
  return jsonify({"message": "Device created", "data": device}), 200


@device_bp.route("/<device_id>", methods=["GET"])
def list_device(device_id):
  device = get_device(device_id)
  if not device:
    return jsonify({"error": "Device not found"}), 404
  return jsonify(device)


@device_bp.route("/update/<device_id>", methods=["PUT"])
@require_api_key
def update_device(device_id):
  data = request.json
  validated = validate_request(device_schema, data)
  if "errors" in validated:
    return jsonify(validated), 400
  
  updated = update(device_id, validated)
  
  if not updated:
    return jsonify({"error": "Device not found"}), 404
  
  app.socketio.emit(
    "device_updated",
    {
      "device_id": updated["id"],
      "state": updated["state"],
      "last_updated": updated["last_updated"]
    }
  )

  logging.info("Device updated: %s", updated["id"])

  log_audit_event(
    user=get_jwt_identity(),
    action="UPDATE_DEVICE",
    resource=updated["id"],
    details=updated
  )
  
  return jsonify({"message": "Device update", "data": updated})


@device_bp.route("/patch/<device_id>", methods=["PATCH"])
@require_api_key
def partial_update(device_id):
  data = request.json
  
  # allow any subfield of a device
  validated = validate_request(patch_schema, data)
  if "errors" in validated:
    return jsonify(validated), 400
  
  updated = patch(device_id, validated)
  if not updated:
    return jsonify({"error": "Device not found"}), 404
  
  app.socketio.emit(
    "device_partially_updated",
    {
      "device_id": updated["id"],
      "state": updated["state"],
      "last_updated": updated["last_updated"]
    }
  )
  
  return jsonify({"message": "Device patched", "data": updated})


@device_bp.route("/del/<device_id>", methods=["DELETE"])
@jwt_required()
@require_role("admin")
def delete(device_id):
  deleted= delete_device(device_id)
  
  if not deleted:
    return jsonify({"error": "Device not found"}), 404
  
  app.socketio.emit("Device_deleted", {"device_id": device_id})
  
  logging.warning("Device deleted: %s", device_id)

  log_audit_event(
    user=get_jwt_identity(),
    action="DELETE_DEVICE",
    resource=device_id
  )
  
  return jsonify({"message": "Device deleted"})


@device_bp.route("/<device_id>/command/", methods=["POST"])
@require_api_key
def command_device(device_id):
  command = request.json
  
  result = send_command_to_device(device_id, command)
  
  if result is None:
    return jsonify({"error": "Device not found"}), 404
  
  if "error" in result:
    return jsonify(result), 400
  
  logging.info("Command sent to device %s", device_id)

  log_audit_event(
    user=get_jwt_identity(),
    action="COMMAND_DEVICE",
    resource=device_id,
    details=result
  )
  
  return jsonify({"message": "Command executed", "result": result})
