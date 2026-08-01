import sys

from qaos.commands.version import execute as version
from qaos.commands.doctor import execute as doctor


def show_help():
    print("QAOS Command Line Interface")
    print()
    print("Available commands:")
    print("  version")
    print("  doctor")
    print("  help")


def main():
    if len(sys.argv) == 1:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "version":
        version()

    elif command == "doctor":
        doctor()

    elif command == "help":
        show_help()

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()