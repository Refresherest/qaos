import sys

from qaos.kernel.kernel import Kernel
from qaos.commands.registry import COMMANDS


COMMAND_DESCRIPTIONS = {
    "about": "Display information about QAOS",
    "agents": "List registered agents",
    "bootstrap": "Validate project structure",
    "council": "Display Executive Council",
    "doctor": "Check development environment",
    "objective": "Execute one objective in an explicit workspace",
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
    print("    python -m qaos.main objective --workspace <path> <goal>")
    print()
    print("Available commands:")
    print()

    for command in sorted(set(COMMANDS) | {"objective"}):
        description = COMMAND_DESCRIPTIONS.get(command, "")
        print(f"  {command:<11} {description}")


def execute_objective_command(workspace, goal):
    from qaos.commands.objective import execute

    return execute(workspace, goal)


def _execute_objective(args):
    if len(args) < 4 or args[1] != "--workspace":
        print(
            "Usage: python -m qaos.main objective "
            "--workspace <path> <goal>",
            file=sys.stderr,
        )
        return 2

    workspace = args[2]
    goal = " ".join(args[3:])

    if not workspace.strip() or not goal.strip():
        print(
            "Usage: python -m qaos.main objective "
            "--workspace <path> <goal>",
            file=sys.stderr,
        )
        return 2

    try:
        result = execute_objective_command(workspace, goal)
    except Exception as exc:
        print(f"Objective execution failed: {exc}", file=sys.stderr)
        return 1

    return 0 if result.completed else 1


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)

    if not args:
        show_help()
        return 0

    command = args[0].lower()

    if command == "help":
        show_help()
        return 0

    if command == "objective":
        return _execute_objective(args)

    if command not in COMMANDS:
        print(f"Unknown command: {command}")
        return 0

    kernel = Kernel()

    if command == "run":
        if len(args) < 2:
            print("Usage: python -m qaos.main run <agent>")
            return 0

        kernel.execute(command, args[1])
    else:
        kernel.execute(command)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
