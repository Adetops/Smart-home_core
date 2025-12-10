from marshmallow import Schema, fields, ValidationError

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



# device validation schema
class DeviceSchema(Schema):
  name = fields.String(required=True)
  type = fields.String(required=True)
  location = fields.String(required=True)
  state = fields.Dict(required=True)

# For PUT where all fields must be present
device_schema = DeviceSchema()

#for PATCH where fields are optional
patch_schema = DeviceSchema(partial=True)

# A helper function to wrap validation
def validate_request(schema, data):
  try:
    return schema.load(data)    # validate & return cleaned data
  except ValidationError as error:
    return {"errors": error.messages}   # return errors to route
