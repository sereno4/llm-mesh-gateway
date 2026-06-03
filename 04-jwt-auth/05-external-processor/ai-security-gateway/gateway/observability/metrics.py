from prometheus_client import Counter, Gauge, generate_latest

soc_requests_total = Counter("soc_requests_total", "Total requests processed")
soc_blocked_total = Counter("soc_blocked_total", "Blocked requests")
soc_risk_score = Gauge("soc_risk_score", "Latest risk score")

def record_event(event: dict):
    soc_requests_total.inc()

    risk = event.get("risk", {})
    score = risk.get("score", 0)

    soc_risk_score.set(score)

    if event.get("action") == "BLOCK":
        soc_blocked_total.inc()

def metrics_endpoint():
    return generate_latest()
