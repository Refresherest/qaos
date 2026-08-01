import sys

from qaos.council import EXECUTIVE_COUNCIL


def execute():
    if len(sys.argv) < 3:
        print("Usage:")
        print("    python -m qaos.main run <agent>")
        return

    name = sys.argv[2].lower()

    member = EXECUTIVE_COUNCIL.get(name)

    if member is None:
        print(f"Unknown agent: {name}")
        return

    member.run()