from gateway.alerts.engine import send_alert

def decide(risk: dict, rule: dict, event: dict):

    action = rule["action"] if rule else "ALLOW"

    # override SOC safety
    if risk["level"] == "CRITICAL":
        action = "BLOCK"

    return {
        "action": action,
        "rule": rule["rule"] if rule else None,
        "reason": rule.get("reason", "") if rule else ""
    }
