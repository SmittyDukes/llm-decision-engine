import json
from datetime import datetime,timezone
import os


LOG_FILE = "logs/decision_logs.jsonl"

# ensure logs directory exists
os.makedirs("logs", exist_ok=True)

def log_event(event: dict):
    print("LOG_EVENT CALLED")
    print("Writing to:", LOG_FILE)
    entry = {**event, "timestamp": datetime.now(timezone.utc).isoformat()}
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print("WRITE COMPLETE")