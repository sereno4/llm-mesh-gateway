def calculate(
    prompt_score: int,
    jailbreak_score: int,
    pii_score: int,
    exfil_score: int,
    tool_score: int = 0,
    agentic_score: int = 0
):
    """
    Risk engine central do gateway.
    Evolutivo para novos detectores sem quebrar assinatura.
    """

    total = (
        prompt_score +
        jailbreak_score +
        pii_score +
        exfil_score +
        tool_score +
        agentic_score
    )

    # normalização defensiva
    if total > 100:
        total = 100

    if total >= 80:
        level = "CRITICAL"
    elif total >= 40:
        level = "HIGH"
    elif total >= 20:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "score": total,
        "level": level
    }
