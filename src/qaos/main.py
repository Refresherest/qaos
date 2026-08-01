import sys

from qaos.commands.registry import COMMANDS


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

    descriptions = {
        "about": "Display information about QAOS",
        "bootstrap": "Validate project structure",
        "doctor": "Check development environment",
        "version": "Display QAOS version",
        "help": "Show this help screen",
    }

    for command in sorted(descriptions):
        print(f"  {command:<12}{descriptions[command]}")


def main():
    if len(sys.argv) == 1:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "help":
        show_help()
        return

    handler = COMMANDS.get(command)

    if handler:
        handler()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()