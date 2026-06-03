def evaluate(
    prompt,
    jailbreak,
    pii,
    exfil,
    tool,
    agentic,
    risk
):

    reasons = []

    if exfil["score"] >= 50:
        reasons.append("data_exfiltration")

    if tool["score"] >= 70:
        reasons.append("tool_abuse")

    if agentic["score"] >= 70:
        reasons.append("agentic_abuse")

    if risk["level"] == "CRITICAL":
        reasons.append("critical_risk")

    return {
        "blocked": len(reasons) > 0,
        "reasons": reasons
    }
