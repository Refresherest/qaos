"""
QAOS Event Bus
"""

from qaos.events.registry import event_registry


class EventBus:

    def __init__(self, registry=None):
        self._registry = registry or event_registry

    def subscribe(self, event_name, handler):
        self._registry.subscribe(event_name, handler)

    def publish(self, event):
        for handler in self._registry.handlers(event.name):
            handler(event)

    def handlers(self, event_name):
        return self._registry.handlers(event_name)

    def all(self):
        return self._registry.all()

    def clear(self):
        self._registry.clear()


event_bus = EventBus()
