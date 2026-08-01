class EventBus:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_name, handler):
        if event_name not in self._listeners:
            self._listeners[event_name] = []

        self._listeners[event_name].append(handler)

    def publish(self, event_name, data=None):
        handlers = self._listeners.get(event_name, [])

        for handler in handlers:
            handler(data)


event_bus = EventBus()