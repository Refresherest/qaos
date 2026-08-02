"""
QAOS Logging Service
"""

from datetime import datetime


class Logger:
    """
    Central logging service for QAOS.
    """

    def info(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[INFO] {timestamp} - {message}")

    def warning(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[WARNING] {timestamp} - {message}")

    def error(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[ERROR] {timestamp} - {message}")


_logger = Logger()


def get_logger():
    """
    Returns the shared QAOS logger instance.
    """
    return _logger