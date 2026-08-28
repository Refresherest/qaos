"""
QAOS Event Registry
"""

class EventRegistry:
    """Subscriber state owned by one event-system lifecycle."""

    def __init__(self):
        self._events = {}

    def subscribe(self, event_name, handler):
        self._events.setdefault(event_name, []).append(handler)

    def handlers(self, event_name):
        return self._events.get(event_name, [])

    def all(self):
        return self._events

    def clear(self):
        self._events.clear()


event_registry = EventRegistry()
EVENTS = event_registry.all()


def subscribe(event_name, handler):
    event_registry.subscribe(event_name, handler)


def handlers(event_name):
    return event_registry.handlers(event_name)
