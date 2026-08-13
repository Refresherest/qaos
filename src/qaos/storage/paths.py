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

MEMORY = DATA / "memory.json"

KNOWLEDGE = DATA / "knowledge.json"

ARTIFACTS = DATA / "artifacts.json"

OBJECTIVES = DATA / "objectives.json"

REFLECTIONS = DATA / "reflections.json"

EVENTS = DATA / "events.json"

PLANS = DATA / "plans.json"

QUEUE = DATA / "queue.json"