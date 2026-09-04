import sys

from qaos.kernel.kernel import Kernel
from qaos.commands.registry import COMMANDS


COMMAND_DESCRIPTIONS = {
    "about": "Display information about QAOS",
    "agents": "List registered agents",
    "bootstrap": "Validate project structure",
    "build-project": "Build an explicitly enabled trusted v2 project",
    "council": "Display Executive Council",
    "doctor": "Check development environment",
    "objective": "Execute one objective in an explicit workspace",
    "objectives": "List objectives in an explicit workspace",
    "recover": "Recover one identified failed objective in an explicit workspace",
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
    print("    python -m qaos.main objectives --workspace <path>")
    print("    python -m qaos.main recover --workspace <path> <objective_id>")
    from qaos.commands.build_project import USAGE
    print("    " + USAGE.removeprefix("Usage: "))
    print()
    print("Available commands:")
    print()

    for command in sorted(set(COMMANDS) | {"objective", "objectives", "recover", "build-project"}):
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
        print(f"Objective execution failed ({type(exc).__name__}).", file=sys.stderr)
        return 1

    return 0 if result.completed else 1


def _recover_objective(args):
    if (len(args) != 4 or args[1] != "--workspace"
            or not args[2].strip() or not args[3].strip()):
        print("Usage: python -m qaos.main recover --workspace <path> <objective_id>",
              file=sys.stderr)
        return 2

    from qaos.commands.recover import execute

    try:
        execute(args[2], args[3])
    except Exception as exc:
        # Exception payloads can contain provider or credential material.
        print(f"Objective recovery failed ({type(exc).__name__}).", file=sys.stderr)
        return 1
    return 0


def _list_objectives(args):
    if len(args) != 3 or args[1] != "--workspace" or not args[2].strip():
        print("Usage: python -m qaos.main objectives --workspace <path>",
              file=sys.stderr)
        return 2
    from qaos.commands.objectives import execute
    try:
        execute(args[2])
    except Exception as exc:
        print(f"Objective listing failed ({type(exc).__name__}).", file=sys.stderr)
        return 1
    return 0


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

    if command == "build-project":
        from qaos.commands.build_project import execute
        return execute(args[1:])

    if command == "objectives":
        return _list_objectives(args)

    if command == "recover":
        return _recover_objective(args)

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
