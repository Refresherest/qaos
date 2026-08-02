import sys

from qaos.kernel import Kernel


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
    print("  about       Display information about QAOS")
    print("  agents      List registered agents")
    print("  bootstrap   Validate project structure")
    print("  council     Display Executive Council")
    print("  doctor      Check development environment")
    print("  help        Show this help screen")
    print("  run         Execute an agent")
    print("  version     Display QAOS version")


def main():
    if len(sys.argv) == 1:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "help":
        show_help()
        return

    kernel = Kernel()

    kernel.execute(command)


if __name__ == "__main__":
    main()