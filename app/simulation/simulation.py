import threading
import time
# from datetime import datetime, timezone
from app.services.service import get_devices, update
# from app.utils.temp import get_temperature

# -----------------------------
# DEVICE SIMULATION LOGIC
# -----------------------------
def simulate_device_behavior(device):
  """
  Simulates the behavior of a single device based on its type.
  """
  state = device.get("state", {})
  device_type = device.get("type")
  updated = False  # Track if state changes

  # ---------- SENSOR ----------
  if device_type in ["sensor", "temperature_sensor"]:
    temp = state.get("temperature", 25)
    temp += 0.5
    if temp > 35:
      temp = 25
    if state.get("temperature") != round(temp, 1):
      state["temperature"] = round(temp, 1)
      updated = True
      print(f"Sensor {device['id']} temperature updated to {state['temperature']}")

  # ---------- LIGHT ----------
  if device_type == "light":
    # Initialize state keys if missing
    if "on" not in state:
      state["on"] = "false"
      state["last_changed"] = time.time()
    if "last_changed" not in state:
      state["last_changed"] = time.time()

    now = time.time()
    on_value = state["on"] in [True, "true", "True"]

    if on_value:
      # Currently ON → check if 10s elapsed
      if now - state["last_changed"] >= 10:
        state["on"] = "false"
        state["last_changed"] = now

        # OFF flags
        state["off_since"] = now

        # Remove ON flags
        state.pop("on_since", None)

        print(f"Light {device['id']} auto-turned OFF after 10s")

    else:
      # Currently OFF → check if 2s elapsed
      if now - state["last_changed"] >= 2:
        state["on"] = "true"
        state["last_changed"] = now

        # ON flags
        state["on_since"] = now

        # Remove OFF flags
        state.pop("off_since", None)

        print(f"Light {device['id']} auto-turned ON after 2s")

    # Persist changes
    update(device["id"], {"state": state})


  # ---------- MOTION SENSOR ----------
  if device_type == "motion_sensor":
    if state.get("motion") is True:
      last = state.get("triggered_at", time.time())
      if time.time() - last > 5:
        state["motion"] = False
        updated = True
        print(f"Motion sensor {device['id']} reset")

  # Persist changes to DB if anything updated
  if updated:
    try:
      updated_device = update(device["id"], {"state": state})
      print(f"Device {device['id']} updated in DB: {updated_device['state']}")
    except Exception as e:
      print(f"Error updating device {device['id']}: {e}")


# -----------------------------
# BACKGROUND SIMULATION LOOP
# -----------------------------
def simulation_loop():
  """
  Loops over all devices every 2 seconds to simulate behavior.
  """
  while True:
    try:
      devices = get_devices()
      print(f"Fetched {len(devices)} devices")
      for device in devices:
        simulate_device_behavior(device)
      time.sleep(2)
    except Exception as e:
      print(f"Simulation loop error: {e}")
      time.sleep(2)


# -----------------------------
# START SIMULATION ENGINE
# -----------------------------
def start_simulation_engine():
  """
  Start the simulation loop in a background daemon thread.
  """
  thread = threading.Thread(target=simulation_loop, daemon=True)
  thread.start()
  print("Simulation engine started in background thread.")
