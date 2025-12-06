# marks routes as a package
from flask import Flask
from app.routes.devices import devices_bp

def create_app():
  app = Flask(__name__)
  app.register_blueprint(devices_bp)
  return app
