# For the security of endpoints

import os

API_KEY = "why-do-you-need-password?"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "we-need-a-token")
JWT_EXPIRES_IN = 3600		# Time in seconds

