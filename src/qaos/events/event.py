"""
QAOS Event
"""


class Event:

    def __init__(self, name: str, payload=None):
        self.name = name
        self.payload = payload or {}