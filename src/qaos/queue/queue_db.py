"""
QAOS Queue Database
"""

from .json_database import JsonDatabase


queue_db = JsonDatabase(
    "queue.json"
)