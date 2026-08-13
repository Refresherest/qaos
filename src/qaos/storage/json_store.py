"""
QAOS JSON Store
"""

import json
import os
from pathlib import Path


class StorageDataError(RuntimeError):
    """Raised when an existing storage artifact cannot be decoded safely."""


class JSONStore:

    def __init__(self, path):

        self.path = Path(path)

    def load(self):

        if not self.path.exists():
            return []

        with open(
            self.path,
            "r",
            encoding="utf-8",
        ) as f:

            data = f.read().strip()

            if not data:
                return []

            try:
                return json.loads(data)

            except json.JSONDecodeError as error:
                raise StorageDataError(
                    f"Invalid JSON in storage file: {self.path}"
                ) from error

    def save(self, data):

        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        with open(temporary, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.write("\n")
        os.replace(temporary, self.path)
