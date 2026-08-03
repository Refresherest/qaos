"""
QAOS Event Registry
"""

EVENTS = {}


def subscribe(event_name, handler):
    EVENTS.setdefault(event_name, []).append(handler)


def handlers(event_name):
    return EVENTS.get(event_name, [])