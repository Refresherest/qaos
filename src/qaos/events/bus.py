"""
QAOS Event Bus
"""

from qaos.events.registry import subscribe, handlers


class EventBus:

    def subscribe(self, event_name, handler):
        subscribe(event_name, handler)

    def publish(self, event):
        for handler in handlers(event.name):
            handler(event)


event_bus = EventBus()