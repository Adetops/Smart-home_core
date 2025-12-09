# marks routes as a package
from flask import Flask
from app.routes.devices import device_bp

def create_app():
  app = Flask(__name__)
  app.register_blueprint(device_bp, url_prefix="/devices/")
  return app
