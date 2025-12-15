from flask import jsonify


def rate_limit_exceeded(e):
  return jsonify({
    "error": "rate_limit_exceeded",
    "message": "Too many requests, slow down."
  }), 429
