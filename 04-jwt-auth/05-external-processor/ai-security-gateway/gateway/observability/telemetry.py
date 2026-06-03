from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

provider = TracerProvider()

processor = BatchSpanProcessor(
    ConsoleSpanExporter()
)

provider.add_span_processor(processor)

trace.set_tracer_provider(provider)

tracer = trace.get_tracer("ai-security-gateway")


def start_span(name: str, attributes: dict = None):
    span = tracer.start_span(name)

    if attributes:
        for k, v in attributes.items():
            span.set_attribute(k, str(v))

    return span
