"""Tracing enriquecido para MLOps — spans com atributos de segurança"""
from opentelemetry import trace
from opentelemetry.trace import SpanKind
import json

tracer = trace.get_tracer("ai-security-gateway.security")

def trace_analyze(prompt: str, result: dict, context: dict = None):
    """Cria span enriquecido com todos os atributos MLOps relevantes"""
    with tracer.start_as_current_span(
        "security.analyze",
        kind=SpanKind.SERVER
    ) as span:
        # Input
        span.set_attribute("llm.input.prompt", prompt[:500])
        span.set_attribute("llm.input.prompt_length", len(prompt))

        # Risk
        risk = result.get("risk", {})
        span.set_attribute("security.risk_score", risk.get("score", 0))
        span.set_attribute("security.risk_level", risk.get("level", "UNKNOWN"))

        # Decision
        decision = result.get("decision", {})
        span.set_attribute("security.action", decision.get("action", "UNKNOWN"))
        span.set_attribute("security.blocked", result.get("blocked", False))
        span.set_attribute("security.rule", decision.get("rule") or "none")
        span.set_attribute("security.reason", decision.get("reason") or "none")

        # Detections
        detections = result.get("detections", {})
        for detector, data in detections.items():
            score = data.get("score", 0) if isinstance(data, dict) else 0
            span.set_attribute(f"security.detection.{detector}", score)

        # Context
        if context:
            span.set_attribute("user.id", context.get("user_id", "anonymous"))
            span.set_attribute("user.role", context.get("role", "guest"))
            span.set_attribute("env", context.get("env", "dev"))

        return result
