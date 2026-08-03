"""
QAOS JSON Persistence Backend
"""

import json
from pathlib import Path

from .database import Database


class JSONStore(Database):

    def __init__(self, filename="qaos.json"):
        self.path = Path(filename)

        if not self.path.exists():
            self.path.write_text("{}")

    def _read(self):
        return json.loads(
            self.path.read_text()
        )

    def _write(self, data):
        self.path.write_text(
            json.dumps(
                data,
                indent=4
            )
        )

    def save(self, key, value):
        data = self._read()

        data[key] = value

        self._write(data)

    def load(self, key):
        data = self._read()

        return data.get(key)

    def delete(self, key):
        data = self._read()

        if key in data:
            del data[key]

        self._write(data)

    def all(self):
        return self._read()