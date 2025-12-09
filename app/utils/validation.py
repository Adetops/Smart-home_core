# defines lists of allowed features

ALLOWED_FIELDS = ["id", "name", "type", "location", "state"]
ALLOWED_TYPES = ["light", "thermostat", "sensor", "switch"]
STATE_FEATURES = ["On/Off", "temperature", "sensor reading", "brightness"]

def validate_device_data(data, required=False):
  errors = []
  
  # Check that required fields are complete
  if required:
    for field in ALLOWED_FIELDS:
      if field not in data:
        errors.append(f'Missing required field: {field}')
  
  # check that data types match
  if "name" in data and not isinstance(data["name"], str):
    errors.append("Field 'name' must be a string")
  if "type" in data and data["type"] not in ALLOWED_TYPES:
    errors.append(f'Field "type" must be one of {ALLOWED_TYPES}')
  if "location" in data and not isinstance(data["location"], str):
    errors.append("Field 'location' must be a string")
  if "state" in data and not isinstance(data["state"], dict):
    errors.append("Field 'state' must be a dictionary")
  # for key in data["state"]:
  #   if key not in STATE_FEATURES:
  #     errors.append(f'{key} state not registered')
  return errors
