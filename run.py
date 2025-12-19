# Initiates the app
import eventlet
eventlet.monkey_patch()

from app import create_app
from app.extensions import socketio
from app.simulation.simulation import start_simulation_engine

app = create_app()


if __name__ == "__main__":
  start_simulation_engine()
  port = int(os.environ.get("PORT", 5000))
  socketio.run(app, host="0.0.0.0", port=port, debug=True, allow_unsafe_werkzeug=True)
