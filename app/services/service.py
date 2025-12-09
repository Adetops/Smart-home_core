from app.models.model import Device
from app.models.schema import validate_payload
from datetime import datetime, timezone

# DEVICES = []
# DEVICE_ID_COUNTER = 1
devices = {}

# def current_timestamp():
#   return datetime.now(timezone.utc).isoformat()

class DeviceService:
  
  @staticmethod
  def get_all():
    return [device.to_dict() for device in devices.values()]
  
  
  @staticmethod
  def get_device(device_id):
    return devices.get(device_id)
  
  
  @staticmethod
  def add_device(data):
    new_device = Device(
      device_id = data["id"],
      name = data["name"],
      type = data["type"],
      location = data["location"],
      state = data.get("state", "off")
    )
  
    devices[new_device.id] = new_device
    return new_device.to_dict()
  
  
  @staticmethod
  def update(device_id, data):
    device = devices.get(device_id)
    if not device:
      return None
    
    device.name = data.get("name", device.name)
    device.type = data.get("type", device.type)
    device.location = data.get("location", device.location)
    device.state = data.get("state", device.state)
    
    return device.to_dict()


@staticmethod
def delete_device(device_id):
  if device_id in devices:
    del devices[device_id]
    return True
  return False
