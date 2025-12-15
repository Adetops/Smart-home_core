from datetime import datetime, timezone
import json
import os


AUDIT_LOG_FILE = "logs/audit.log"


def log_audit_event(user, action, resource, details=None):
  """
  Writes immutable audit records.
  """

  os.makedirs("logs", exist_ok=True)

  record = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "user": user,
    "action": action,
    "resource": resource,
    "details": details or {}
  }

  with open(AUDIT_LOG_FILE, "a") as file:
    file.write(json.dumps(record) + "\n")
