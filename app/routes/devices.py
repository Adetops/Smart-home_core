# Blueprints for Home devices
from flask import Blueprint, request, jsonify
from app.controllers.controller import DeviceController


device_bp = Blueprint("devices", __name__)


device_bp.route("/", methods=["GET"])(DeviceController.get_all)
device_bp.route("/", methods=["POST"])(DeviceController.create_new)
device_bp.route("/<device_id>", methods=["GET"])(DeviceController.get_one)
device_bp.route("/<device_id>", methods=["PUT"])(DeviceController.update_device)
device_bp.route("/<device_id>", methods=["DELETE"])(DeviceController.delete_device)
