# marks routes as a package
from flask import Flask
from flask_jwt_extended import JWTManager
from app.routes.devices import device_bp
from app.routes.auth import auth_bp
from app.config.security import JWT_SECRET_KEY
from app.utils.logger import setup_logger
from app.extensions import limiter, socketio
from app.utils.rate_limiter import rate_limit_exceeded
from flasgger import Swagger

jwt = JWTManager()

swagger = Swagger()

def create_app():
  app = Flask(__name__)
  app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

  app.config["SWAGGER"] = {
    "title": "SmartHome Core API",
    "uiversion": 3
  }

  jwt.init_app(app)
  
  app.register_blueprint(device_bp, url_prefix="/devices")
  app.register_blueprint(auth_bp, url_prefix="/auth")
  
  setup_logger()
  socketio.init_app(app)
  
  from app.routes import socket_events
  
  limiter.init_app(app)
  app.register_error_handler(429, rate_limit_exceeded)
  
  swagger.init_app(app)
  
  return app
