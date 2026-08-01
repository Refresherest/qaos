import sys

from qaos.commands.registry import COMMANDS


def show_help():
    print("QAOS Command Line Interface")
    print()
    print("Available commands:")

    for command in sorted(COMMANDS):
        print(f"  {command}")

    print("  help")


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