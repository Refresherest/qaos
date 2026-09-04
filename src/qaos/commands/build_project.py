"""Explicit operator opt-in adapter for the existing trusted v2 builder."""
from pathlib import Path
import sys

from qaos.application import OperationalSession
from qaos.capabilities.python_project import reject_reparse, require_local_ntfs
from qaos.planner import PythonProjectIntentV2
from qaos.storage import create_stores


USAGE = ("Usage: python -m qaos.main build-project --workspace <state> "
         "--output-root <output> --directory <name> --metrics <words,lines> "
         "--enable-project text_stats_project_v2")
OPTIONS = frozenset(("--workspace", "--output-root", "--directory",
                     "--metrics", "--enable-project"))


def parse(args):
    if len(args) != 2 * len(OPTIONS):
        raise ValueError("invalid option count")
    values = {}
    for key, value in zip(args[::2], args[1::2]):
        if key not in OPTIONS or key in values or not value.strip() or value.startswith("--"):
            raise ValueError("invalid option")
        values[key] = value
    if values["--enable-project"] != "text_stats_project_v2":
        raise ValueError("explicit v2 permission required")
    intent = PythonProjectIntentV2(values["--directory"], values["--metrics"].split(","))
    return values["--workspace"], values["--output-root"], intent


def validate_roots(workspace, output):
    roots = (Path(workspace), Path(output))
    for root in roots:
        if not root.is_absolute() or not root.is_dir():
            raise ValueError("existing absolute roots required")
        # Check the supplied spelling before resolution can hide reparse traversal.
        reject_reparse(root)
    state, target = (root.resolve(strict=True) for root in roots)
    if state == target or state in target.parents or target in state.parents:
        raise ValueError("roots must not overlap")
    require_local_ntfs(target)
    return state, target


def execute(args):
    try:
        workspace, output, intent = parse(args)
    except (ValueError, TypeError):
        print(USAGE, file=sys.stderr)
        return 2
    try:
        state, target = validate_roots(workspace, output)
        session = OperationalSession(create_stores(state), python_project_workspace=target,
                                     enabled_python_projects=("text_stats_project_v2",))
        objective = session.create_objective("plan configured trusted project")
        print(f"Objective ID: {objective.objective_id}", flush=True)
        result = session.execute_intent(objective, intent)
        print(f"Status: {'completed' if result.completed else 'failed'}")
        if not result.completed:
            return 1
        print(f"Published directory: {target / intent.relative_directory}")
        print(f"Metrics: {','.join(intent.metrics)}")
        return 0
    except Exception as exc:
        print("Status: failed")
        print(f"Project build failed ({type(exc).__name__}).", file=sys.stderr)
        return 1
