"""
QAOS Database
"""

from .json_store import JSONStore

from .paths import (
    MEMORY,
    KNOWLEDGE,
    ARTIFACTS,
    OBJECTIVES,
    REFLECTIONS,
    EVENTS,
    PLANS,
    QUEUE,
)

memory_db = JSONStore(MEMORY)

knowledge_db = JSONStore(KNOWLEDGE)

artifact_db = JSONStore(ARTIFACTS)

objective_db = JSONStore(OBJECTIVES)

reflection_db = JSONStore(REFLECTIONS)

event_db = JSONStore(EVENTS)

plan_db = JSONStore(PLANS)

queue_db = JSONStore(QUEUE)