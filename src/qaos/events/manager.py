"""
QAOS Event Manager
"""

from qaos.events.bus import event_bus
from qaos.events.event import Event
from qaos.events.registry import (
    subscribe,
    handlers,
    EVENTS,
)


class EventManager:

    def subscribe(self, name, handler):
        subscribe(name, handler)

    def emit(self, name, payload=None):
        event = Event(name, payload)
        event_bus.publish(event)

    def publish(self, event):
        event_bus.publish(event)

    def handlers(self, name):
        return handlers(name)

    def all(self):
        return EVENTS

    def clear(self):
        EVENTS.clear()


event_manager = EventManager()