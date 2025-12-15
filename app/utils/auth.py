# For Routes authentication

from functools import wraps
from flask import request, jsonify
from app.config.security import API_KEY


def require_api_key(func):
  """
  Decorator that protects endpoints using an API key
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    client_key = request.headers.get("X-API-Key")
    
    if not client_key:
      return jsonify({"error": "API key missing"}), 401
    
    if client_key != API_KEY:
      return jsonify({"error": "Invalid API key"}), 403
    
    return func(*args, **kwargs)
  return wrapper
