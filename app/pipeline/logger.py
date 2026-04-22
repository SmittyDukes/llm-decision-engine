import json
from datetime import datetime, timezone
import os


LOG_FILE = "logs/decision_logs.jsonl"

# ensure logs directory exists
os.makedirs("logs", exist_ok=True)

def log_event(event: dict):
    entry = {**event, "timestamp": datetime.now(timezone.utc).isoformat()}
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")