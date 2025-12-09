class Device:
  def __init__(self, device_id, name, type, location, state):
    self.id = device_id
    self.name = name
    self.type = type
    self.location = location
    self.state = state
    self.last_updated = None
  
  def to_dict(self):
    return {
			"id": self.id,
			"name": self.name,
			"type": self.type,
			"location": self.location,
			"state": self.state,
			"last_updated": self.last_updated
		}
