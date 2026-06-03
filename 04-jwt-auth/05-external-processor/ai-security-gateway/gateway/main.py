from fastapi import FastAPI
from gateway.policy_engine.engine import evaluate
from gateway.observability.tracing import trace_analyze
from gateway.observability.metrics import record_event, metrics_endpoint
from gateway.siem.exporter import store_event

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from phoenix.otel import register

app = FastAPI()

# =========================
# 🔥 PHOENIX / ARIZE TRACING
# =========================
tracer_provider = register(
    project_name="ai-security-gateway"
)

FastAPIInstrumentor.instrument_app(app)

# =========================
# ROUTES
# =========================

@app.post("/analyze")
def analyze(payload: dict):
    prompt = payload.get("prompt", "")

    # policy engine
    result = evaluate({"prompt": prompt})
    trace_analyze(prompt, result)

    # SIEM
    store_event({
        "prompt": prompt,
        "risk": result.get("risk", {}),
        "decision": result.get("action", "ALLOW"),
    })

    # metrics (Prometheus)
    record_event(result)

    return {
        "trace_id": payload.get("trace_id"),
        "prompt": prompt,
        "risk": result.get("risk", {}),
        "decision": result,
        "blocked": result.get("action") == "BLOCK"
    }


@app.get("/metrics")
def metrics():
    from fastapi.responses import Response
    return Response(content=metrics_endpoint(), media_type="text/plain; version=0.0.4")
