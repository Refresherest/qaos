"""
QAOS Council Lifecycle
"""

from qaos.events import event_manager
from qaos.council import council_manager


def initialize_council(event):
    council_manager.initialize()


def shutdown_council(event):
    council_manager.shutdown()


event_manager.subscribe(
    "runtime.started",
    initialize_council,
)

event_manager.subscribe(
    "runtime.stopping",
    shutdown_council,
)