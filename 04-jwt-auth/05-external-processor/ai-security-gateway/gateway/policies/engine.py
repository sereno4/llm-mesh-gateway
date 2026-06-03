def evaluate_risk(score: int) -> str:
    """
    Central policy engine (future OPA replacement)
    """

    if score >= 80:
        return "CRITICAL"
    elif score >= 40:
        return "HIGH"
    elif score >= 20:
        return "MEDIUM"
    else:
        return "LOW"


def should_block(level: str) -> bool:
    return level in ["HIGH", "CRITICAL"]
