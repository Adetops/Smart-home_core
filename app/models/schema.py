from marshmallow import Schema, fields, ValidationError

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
