def compute_risk(prompt_score, jailbreak_score, pii_score, exfil_score, tool_score):

    risk_score = (
        prompt_score * 0.30 +
        jailbreak_score * 0.20 +
        pii_score * 0.20 +
        exfil_score * 0.25 +
        tool_score * 0.25
    )

    risk_score = min(risk_score, 100)

    if risk_score >= 85:
        level = "CRITICAL"
    elif risk_score >= 60:
        level = "HIGH"
    elif risk_score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "score": round(risk_score, 2),
        "level": level
    }
