# marks routes as a package
from flask import Flask
from flask_jwt_extended import JWTManager
from app.routes.devices import device_bp
from app.routes.auth import auth_bp
from app.config.security import JWT_SECRET_KEY
from app.utils.logger import setup_logger


jwt = JWTManager()

def create_app():
  app = Flask(__name__)
  app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

  jwt.init_app(app)
  app.register_blueprint(device_bp, url_prefix="/devices")
  app.register_blueprint(auth_bp, url_prefix="/auth")
  setup_logger()
  
  return app
