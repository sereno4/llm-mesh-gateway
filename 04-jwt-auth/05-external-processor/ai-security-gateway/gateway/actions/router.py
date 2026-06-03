from gateway.siem.store import write_event
from gateway.alerts.engine import send_alert

def route_action(result: dict, event: dict):

    action = result.get("action", "ALLOW")
    risk_level = event.get("risk", {}).get("level", "LOW")

    # sempre loga no SIEM
    write_event(event)

    # BLOQUEIO
    if action == "BLOCK":
        if risk_level in ["HIGH", "CRITICAL"]:
            send_alert(event)
        return "BLOCKED"

    # ALERT ONLY (casos futuros)
    if action == "ALERT":
        send_alert(event)
        return "ALERTED"

    return "ALLOWED"
