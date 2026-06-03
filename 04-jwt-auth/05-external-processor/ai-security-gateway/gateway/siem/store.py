import json
import time
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_FILE = os.path.join(BASE_DIR, "siem_events.jsonl")


def write_event(event: dict):
    event = dict(event)

    event["ts"] = time.time()
    event["source"] = "soc-level-4"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    print("[SIEM] event stored")
