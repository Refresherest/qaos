import sys

from qaos.kernel.kernel import Kernel
from qaos.commands.registry import COMMANDS


COMMAND_DESCRIPTIONS = {
    "about": "Display information about QAOS",
    "agents": "List registered agents",
    "bootstrap": "Validate project structure",
    "council": "Display Executive Council",
    "doctor": "Check development environment",
    "run": "Execute an agent",
    "status": "Display runtime status",
    "version": "Display QAOS version",
}


def show_help():
    print("=" * 50)
    print("QAOS Command Line Interface")
    print("=" * 50)
    print()
    print("Usage:")
    print("    python -m qaos.main <command>")
    print()
    print("Available commands:")
    print()

    for command in sorted(COMMANDS.keys()):
        description = COMMAND_DESCRIPTIONS.get(command, "")
        print(f"  {command:<11} {description}")


def main():
    kernel = Kernel()

    if len(sys.argv) == 1:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "help":
        show_help()
        return

    if command not in COMMANDS:
        print(f"Unknown command: {command}")
        return

    if command == "run":
        if len(sys.argv) < 3:
            print("Usage: python -m qaos.main run <agent>")
            return

        kernel.execute(command, sys.argv[2])
    else:
        kernel.execute(command)


if __name__ == "__main__":
    main()