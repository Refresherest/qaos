from pathlib import Path
from qaos.version import VERSION

class Configuration:
    def __init__(self):
        self.project_root = Path.cwd()
        self.version = VERSION
        self.project_name = "QAOS"

    def get(self, key):
        return getattr(self, key, None)


config = Configuration()