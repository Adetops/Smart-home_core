from app.services.service import DeviceService
from flask import jsonify, request

class DeviceController:
  
  
  @staticmethod
  def get_all():
    return jsonify(DeviceService.get_all()), 200
  
    
  @staticmethod
  def get_one(device_id):
    device = DeviceService.get_device(device_id)
    if device:
      return jsonify(device.to_dict()), 200
    return jsonify({"error": "Device not found"}), 404
  
    
  @staticmethod
  def create_new():
    data = request.json
    new_device = DeviceService.add_device(data)
    return jsonify(new_device)
  
  
  @staticmethod
  def update_device(device_id):
    data = request.json
    updated = DeviceService.update(device_id, data)
    if updated:
      return jsonify(updated), 200
    return jsonify({"error": "Device not found for update"}), 404
    
  
  @staticmethod
  def delete_device(device_id):
    deleted = DeviceService.delete_device(device_id)
    if deleted:
      return jsonify({"message": "Device deletion is successful"}), 200
    return jsonify({"error": "Device not found for deletion"}), 404
