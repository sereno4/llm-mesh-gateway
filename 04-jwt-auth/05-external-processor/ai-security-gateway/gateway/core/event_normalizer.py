import time
import uuid


def normalize(trace_id, prompt, risk, detections, decision, context=None):
    return {
        "trace_id": trace_id or str(uuid.uuid4()),
        "timestamp": time.time(),

        "context": context or {
            "user_id": "anonymous",
            "role": "guest",
            "env": "dev",
            "ip": "127.0.0.1"
        },

        "prompt": prompt,

        "risk": {
            "score": risk.get("score", 0),
            "level": risk.get("level", "LOW")
        },

        "detections": detections or {},

        "decision": decision or {
            "action": "ALLOW",
            "rule": None,
            "reason": ""
        },

        "blocked": decision.get("action") == "BLOCK" if decision else False
    }
