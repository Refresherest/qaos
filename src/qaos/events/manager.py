"""
QAOS Event Manager
"""

from qaos.events.bus import EventBus, event_bus
from qaos.events.event import Event


class EventManager:

    def __init__(self, bus=None, registry=None):
        if bus is not None and registry is not None:
            raise ValueError("provide either bus or registry, not both")

        self._bus = bus or (
            EventBus(registry=registry)
            if registry is not None
            else event_bus
        )

    def subscribe(self, name, handler):
        self._bus.subscribe(name, handler)

    def emit(self, name, payload=None):
        event = Event(name, payload)
        self._bus.publish(event)

    def publish(self, event):
        self._bus.publish(event)

    def handlers(self, name):
        return self._bus.handlers(name)

    def all(self):
        return self._bus.all()

    def clear(self):
        self._bus.clear()


event_manager = EventManager()
