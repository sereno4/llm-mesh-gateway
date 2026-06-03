import requests
import os

WEBHOOK_URL = os.getenv("ALERT_WEBHOOK", "")


def send_alert(event: dict):

    if not WEBHOOK_URL:
        print("[ALERT] webhook not configured")
        return

    payload = {
        "text": f"🚨 SOC ALERT: {event.get('rule')} | {event.get('prompt')}",
        "risk": event.get("risk"),
        "trace_id": event.get("trace_id")
    }

    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=2)
        print("[ALERT] sent")

    except Exception as e:
        print(f"[ALERT ERROR] {e}")
