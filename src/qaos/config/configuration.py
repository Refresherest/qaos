from pathlib import Path


class Configuration:
    def __init__(self):
        self.project_root = Path.cwd()

        self.version = "0.1.0"
        self.environment = "development"

        self.paths = {
            "docs": self.project_root / "docs",
            "src": self.project_root / "src",
            "tests": self.project_root / "tests",
            "runtime": self.project_root / "runtime",
            "logs": self.project_root / "runtime" / "logs",
            "plugins": self.project_root / "plugins",
        }

    def get(self, key):
        return getattr(self, key, None)

    def get_path(self, name):
        return self.paths.get(name)

    def is_development(self):
        return self.environment == "development"


configuration = Configuration()