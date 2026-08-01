import sys


VERSION = "0.1.0"


def show_version():
    print("=" * 50)
    print("QAOS - Qaasim April AI Operating System")
    print(f"Version: {VERSION}")
    print("=" * 50)


def show_help():
    print("QAOS Command Line Interface")
    print()
    print("Available commands:")
    print("  version")
    print("  help")


def main():
    if len(sys.argv) == 1:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "version":
        show_version()
    elif command == "help":
        show_help()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()