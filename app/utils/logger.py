import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logger():
  """
  Configures application-wide logging.
  """

  log_dir = "logs"
  os.makedirs(log_dir, exist_ok=True)

  logger = logging.getLogger()
  logger.setLevel(logging.INFO)
  
  handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=1_000_000,
    backupCount=3
  )

  formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
  )

  handler.setFormatter(formatter)
  logger.addHandler(handler)
