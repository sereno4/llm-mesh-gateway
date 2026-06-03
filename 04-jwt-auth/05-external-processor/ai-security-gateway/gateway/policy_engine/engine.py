import re
import yaml

with open("gateway/policy_engine/policies.yaml") as f:
    POLICIES = yaml.safe_load(f)["rules"]

def evaluate(event: dict):

    prompt = event.get("prompt", "")

    for rule in POLICIES:

        when = rule.get("when", {})
        action = rule.get("action")

        match = True

        for key, condition in when.items():

            value = prompt if key == "prompt" else event.get(key)

            if isinstance(condition, str) and condition.startswith(">="):
                threshold = float(condition.replace(">=", "").strip())
                if float(value or 0) < threshold:
                    match = False

            elif isinstance(condition, str):
                if value is None or not re.search(condition, str(value)):
                    match = False

        if match:
            return {
                "action": action,
                "name": rule.get("name"),
                "reason": rule.get("reason", ""),
                "risk": {
                    "score": 75 if action == "BLOCK" else 10
                }
            }

    return {
        "action": "ALLOW",
        "name": None,
        "reason": "no policy matched",
        "risk": {"score": 5}
    }
