from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from app.services.user_service import create_user, authenticate_user
from app.utils.audit import log_audit_event
import logging


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
  data = request.json
  user = create_user(data["username"], data["password"], data["role"])
  if not user:
    return jsonify({"error": "User already exists"}), 400
  
  logging.info("User registered: %s", data["username"])

  log_audit_event(
    user=data["username"],
    action="REGISTER",
    resource="auth"
  )
  
  return jsonify({"message": "User created", "user": user}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
  data = request.json
  user = authenticate_user(data["username"], data["password"])
  if not user:
    return jsonify({"error": "Invalid login details"}), 401
  
  token = create_access_token(
		identity=str(user["_id"]),
  	additional_claims={"role": user.get("role", "user")}
	)
  
  logging.info("User logged in: %s", data["username"])

  log_audit_event(
    user=data["username"],
    action="LOGIN",
    resource="auth"
  )
  
  return jsonify({"access_token": token})
