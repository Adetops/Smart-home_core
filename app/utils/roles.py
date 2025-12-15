from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity
import logging


def require_role(required_role):
  """
  Restricts access to users with a specific role.
  """

  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      claims = get_jwt()
      user_role = claims.get("role")

      if user_role != required_role:
        logging.warning("User %s attempted %s without sufficient role", get_jwt_identity(), request.path)
        return jsonify({
          "error": "Forbidden",
          "message": f"{required_role} role required"
        }), 403

      return func(*args, **kwargs)

    return wrapper

  return decorator
