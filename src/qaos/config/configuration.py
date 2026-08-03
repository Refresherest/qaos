from pathlib import Path


class Configuration:

    def __init__(self):
        self.project_root = Path.cwd()

        self._values = {
            "version": "0.1.0",
            "environment": "development",
            "database": "sqlite",
            "ai_provider": "mock",
            "log_level": "info",
        }

        self.paths = {
            "docs": self.project_root / "docs",
            "src": self.project_root / "src",
            "tests": self.project_root / "tests",
            "runtime": self.project_root / "runtime",
            "logs": self.project_root / "runtime" / "logs",
            "plugins": self.project_root / "plugins",
        }

    def get(self, key, default=None):
        return self._values.get(key, default)

    def set(self, key, value):
        self._values[key] = value

    def all(self):
        return dict(self._values)

    def get_path(self, name):
        return self.paths.get(name)

    def is_development(self):
        return self.get("environment") == "development"


        
configuration = Configuration()