"""
QAOS Plan Database
"""

from . import JSONStore, DATA_DIR


plan_db = JSONStore(
    DATA_DIR / "plans.json"
)