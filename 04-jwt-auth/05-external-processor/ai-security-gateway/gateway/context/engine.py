from dataclasses import dataclass
import uuid
import time


@dataclass
class RequestContext:
    user_id: str
    role: str
    env: str
    ip: str
    session_id: str
    timestamp: float


def build_context(headers=None) -> RequestContext:
    return RequestContext(
        user_id="anonymous",
        role="guest",
        env="dev",
        ip="127.0.0.1",
        session_id=str(uuid.uuid4()),
        timestamp=time.time()
    )
