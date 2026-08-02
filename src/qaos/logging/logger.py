"""
QAOS Logging Service
"""

from datetime import datetime


class Logger:
    """
    Central logging service for QAOS.
    """

    def _log(self, level: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{level}] {timestamp} - {message}")

    def info(self, message: str):
        self._log("INFO", message)

    def warning(self, message: str):
        self._log("WARNING", message)

    def error(self, message: str):
        self._log("ERROR", message)


logger = Logger()


def get_logger():
    return logger