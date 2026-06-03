from collections import defaultdict, deque
import time

MAX_EVENTS = 20

# client_id -> list of (event, timestamp)
sessions = defaultdict(lambda: deque(maxlen=MAX_EVENTS))

def add_event(client_id: str, event_type: str):
    sessions[client_id].append({
        "event": event_type,
        "ts": time.time()
    })

def get_events(client_id: str):
    return list(sessions[client_id])

def clear_session(client_id: str):
    sessions.pop(client_id, None)
