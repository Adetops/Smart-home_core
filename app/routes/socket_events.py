from flask_socketio import emit
from app import socketio


@socketio.on("connect")
def handle_connect():
  emit("status", {"message": "Successful connection to SmartHome Core"})
  

@socketio.on("disconnect")
def handle_disconnect():
  print("Client disconnected")
