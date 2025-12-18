# app/extensions.py
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO


socketio = SocketIO(cors_allowed_origins="*")

redis_url = os.getenv("REDIS_URL")

limiter = Limiter(
  key_func=get_remote_address,
  storage_uri=redis_url,
  default_limits=["200 per day", "50 per hour"]
)
