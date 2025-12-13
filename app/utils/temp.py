def get_temperature(state, key="temperature", default=25):
  """
  Safely get the numeric temperature from the state dictionary.

  Args:
    state (dict): Dictionary containing sensor data.
    key (str): Key in the dictionary for temperature.
    default (float): Default value if key is missing.

  Returns:
    float: Numeric temperature value.
  """
  temp_raw = state.get(key, default)

  try:
    # If it's a string like "23°C", extract numeric part
    if isinstance(temp_raw, str):
      temp_num = float(''.join(c for c in temp_raw if c.isdigit() or c == '.'))
    else:
      temp_num = float(temp_raw)
  except ValueError:
    # If conversion fails, fallback to default
    temp_num = float(default)

  return temp_num
