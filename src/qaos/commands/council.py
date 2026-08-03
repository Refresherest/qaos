"""
QAOS Council Command
"""

from qaos.council import council_manager


def execute():
    print("=" * 50)
    print("QAOS Executive Council")
    print("=" * 50)
    print()

    for key, member in council_manager.members().items():
        print(f"{key:<30} {member.title}")