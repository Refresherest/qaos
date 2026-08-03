"""
QAOS Run Command
"""

import sys

from qaos.council import council_manager


def execute():
    if len(sys.argv) < 3:
        print("Usage:")
        print("    python -m qaos.main run <member>")
        return

    name = sys.argv[2].lower()

    members = council_manager.members()

    if name not in members:
        print(f"Unknown council member: {name}")
        return

    council_manager.execute(name)