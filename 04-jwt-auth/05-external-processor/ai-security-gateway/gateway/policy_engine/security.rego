package ai.security

default decision = "ALLOW"

# Bloqueio por risco crítico
deny {
    input.risk.level == "CRITICAL"
}

# Bloqueio por agentic abuse
deny {
    input.detections.agentic_abuse.score > 0
}

# Bloqueio por data exfiltration forte
deny {
    input.detections.data_exfiltration.score >= 40
}

# Bloqueio por tool abuse perigoso
deny {
    input.detections.tool_abuse.score >= 35
}

# Kill chain detectado
deny {
    input.correlation.is_attack_chain == true
}

decision = "BLOCK" {
    deny
}
