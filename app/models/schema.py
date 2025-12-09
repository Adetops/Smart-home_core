# database schema

def validate_payload(data: dict):
  required_fields = ["name", "type", "location", "state"]
  
  for field in required_fields:
    if field not in data:
      return False, f"Missing field: {field}"
    
    if not isinstance(data["name"], str):
      return False, "Device name must be a string"
    
    if not isinstance(data["type"], str):
      return False, "Type of device must be a string"
    
    if not isinstance(data["location"], str):
      return False, "Device location must be a string"
    
    if not isinstance(data["state"], dict):
      return False, "Device state must be a dict object"
    
    return True, None
