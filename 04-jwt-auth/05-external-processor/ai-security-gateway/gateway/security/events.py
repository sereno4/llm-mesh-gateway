import json
from datetime import datetime

def emit(event):

    event["timestamp"] = datetime.utcnow().isoformat()

    print(
        json.dumps(
            event,
            ensure_ascii=False
        )
    )
