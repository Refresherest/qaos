"""
QAOS Storage Paths
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

DATA = ROOT / "data"

DATA.mkdir(
    parents=True,
    exist_ok=True,
)

NAMES = {
    "memory": "memory.json",
    "knowledge": "knowledge.json",
    "artifacts": "artifacts.json",
    "objectives": "objectives.json",
    "reflections": "reflections.json",
    "events": "events.json",
    "plans": "plans.json",
    "queue": "queue.json",
}


def path_for(data_dir, name):
    """Resolve the storage file path for a named store within data_dir."""
    return Path(data_dir) / NAMES[name]


MEMORY = DATA / "memory.json"

KNOWLEDGE = DATA / "knowledge.json"

ARTIFACTS = DATA / "artifacts.json"

OBJECTIVES = DATA / "objectives.json"

REFLECTIONS = DATA / "reflections.json"

EVENTS = DATA / "events.json"

PLANS = DATA / "plans.json"

QUEUE = DATA / "queue.json"