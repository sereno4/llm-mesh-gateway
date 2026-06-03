import json
from datetime import datetime

def store_event(event: dict):
    event["ts"] = datetime.utcnow().timestamp()

    with open("gateway/siem_events.jsonl", "a") as f:
        f.write(json.dumps(event) + "\n")
