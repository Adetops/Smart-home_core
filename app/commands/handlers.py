"""
Command handlers for SmartHome devices.
Each device type has its own logic for state updates.
"""


def light_handler(device, command):
  """
  Commands for light devices
	Example:
	{ "action": "on" }
	{ "action": "off" }
  """
  action = command.get("action")
  
  if action == "on":
    device["state"]["on"] = True
  elif action == "off":
    device["state"]["on"] = False
  else:
    return {"error": "Unknown light command"}
  
  return {"status": "ok", "updated_state": device["state"]}



def lock_handler(device, command):
  """
  Commands for door locks
	Example:
	{ "action": "lock" }
	{ "action": "unlock" }
  """
  action = command.get("action")
  
  if action == "lock":
    device["state"]["locked"] = True
  elif action == "unlock":
    device["state"]["locked"] = False
  else:
    return {"error": "Unknown lock command"}
  
  return {"status": "ok", "updated_state": device["state"]}


  
def sensor_handler(device, command):  
  """
  Sensors cannot be commanded directly
  allowed:
  { "action": "calibrate" }
  """
  action = command.get("action")
  
  if action == "calibrate":
    device["state"]["value"] = 0
    return {"status": "ok", "updated_state": device["state"]}

  return {"error": "Sensors don't accept commands"}



# --- ROUTER: selects the correct handler based on device type ---
def dispatch_command(device, command):
  device_type = device.get("type")
  
  if device_type == "light":
    return light_handler(device, command)
  
  elif device_type == "lock":
    return lock_handler(device, command)
  
  elif device_type == "sensor":
    return sensor_handler(device, command)
  
  else:
    return {"error": f"No command handler for device type '{device_type}'"}
