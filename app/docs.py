from flask_restx import Api

api = Api(
  title="SmartHome Core API",
  version="1.0",
  description="Backend API for SmartHome IoT system",
  doc="/docs"
)


# 🔐 JWT support configuration
api.authorizations = {
  "Bearer": {
    "type": "apiKey",
    "in": "header",
    "name": "Authorization",
	}
}

api.security = "Bearer"
