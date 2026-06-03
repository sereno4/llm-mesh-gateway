def correlate(events):
    """
    events: list of {"event": str, "ts": float}
    """

    event_types = [e["event"] for e in events]

    score = 0
    chain = []
    attack_flags = []

    # STEP 1 - reconnaissance
    if "prompt_injection" in event_types:
        score += 20
        chain.append("recon_prompt_injection")

    if "jailbreak" in event_types:
        score += 20
        chain.append("bypass_attempt")

    # STEP 2 - data targeting
    if "pii" in event_types:
        score += 30
        chain.append("pii_probe")

    if "data_exfiltration" in event_types:
        score += 40
        chain.append("data_targeting")

    # STEP 3 - execution / tool abuse
    if "tool_abuse" in event_types:
        score += 40
        chain.append("execution_attempt")

    # STEP 4 - privilege escalation
    if "agentic_abuse" in event_types:
        score += 100
        chain.append("privilege_escalation")
        attack_flags.append("CRITICAL_AGENTIC_ATTACK")

    # BONUS: kill-chain detection
    if (
        "prompt_injection" in event_types and
        "data_exfiltration" in event_types
    ):
        score += 30
        attack_flags.append("DATA_KILL_CHAIN")

    if (
        "tool_abuse" in event_types and
        "agentic_abuse" in event_types
    ):
        score += 50
        attack_flags.append("INFRASTRUCTURE_TAKEOVER_CHAIN")

    return {
        "score": min(score, 100),
        "chain": chain,
        "attack_flags": attack_flags,
        "is_attack_chain": len(attack_flags) > 0
    }
