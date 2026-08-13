#!/usr/bin/env python
"""Read-only, evidence-oriented QAOS architecture inspection.

The tool intentionally reports signals and explicit evidence.  It does not
declare that a finding is a repair authorization.
"""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


TOOL_VERSION = "1.0.0"


def git(repo: Path, *args: str) -> str:
    command = ["git", "-C", str(repo), "-c", f"safe.directory={repo.as_posix()}", *args]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    return (result.stdout or result.stderr).strip()


def python_files(repo: Path) -> list[Path]:
    return sorted((repo / "src" / "qaos").rglob("*.py"))


def source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def lines_for(text: str, needle: str) -> list[int]:
    return [index for index, line in enumerate(text.splitlines(), 1) if needle in line]


def inspect(repo: Path) -> dict:
    files = python_files(repo)
    modules: dict[Path, ast.Module] = {}
    texts: dict[Path, str] = {}
    duplicate_classes: defaultdict[str, list[str]] = defaultdict(list)
    import_time_calls: list[dict] = []

    for path in files:
        text = source(path)
        texts[path] = text
        tree = ast.parse(text, filename=str(path))
        modules[path] = tree
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                duplicate_classes[node.name].append(str(path.relative_to(repo)))
            if isinstance(node, (ast.Assign, ast.AnnAssign)) and isinstance(getattr(node, "value", None), ast.Call):
                import_time_calls.append({"path": str(path.relative_to(repo)), "line": node.lineno})

    findings: list[dict] = []
    for name, paths in sorted(duplicate_classes.items()):
        if len(paths) > 1:
            findings.append({
                "id": f"DUPLICATE-CLASS-{name.upper()}",
                "classification": "review",
                "severity": "P1" if name in {"Objective", "Task", "Memory", "Capability"} else "P2",
                "rule": "ADR-001 / ADR-005A canonical object law",
                "evidence": paths,
                "action": "Reconcile whether these are the same canonical domain concept before changing code.",
            })

    required = {"register", "unregister", "get", "all"}
    registry_checks = []
    for path in sorted((repo / "src" / "qaos").rglob("registry.py")):
        functions = {node.name for node in modules[path].body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        missing = sorted(required - functions)
        registry_checks.append({"path": str(path.relative_to(repo)), "functions": sorted(functions), "missing": missing})
        if missing:
            findings.append({
                "id": f"REGISTRY-{path.parent.name.upper()}",
                "classification": "implementation-violation",
                "severity": "P2",
                "rule": "ADR-003 / ADR-005",
                "evidence": {"path": str(path.relative_to(repo)), "missing": missing},
                "action": "Create a scoped migration work order; do not introduce permanent aliases.",
            })

    patterns = [
        ("PIPELINE-EXECUTION-REFLECTION", repo / "src" / "qaos" / "execution" / "engine.py", "reflection_manager.create", "P0", "ADR-002 / ADR-011I"),
        ("PIPELINE-EXECUTION-LEARNING", repo / "src" / "qaos" / "execution" / "manager.py", "learning_manager.learn", "P0", "ADR-002 / ADR-011I"),
        ("ENTITY-OBJECTIVE-SELF-PERSISTENCE", repo / "src" / "qaos" / "objectives" / "objective.py", "objective_manager._save", "P1", "ADR-001 / ADR-008A / ADR-011J"),
    ]
    for finding_id, path, needle, severity, rule in patterns:
        if path.exists() and (matches := lines_for(texts[path], needle)):
            findings.append({
                "id": finding_id,
                "classification": "implementation-violation",
                "severity": severity,
                "rule": rule,
                "evidence": {"path": str(path.relative_to(repo)), "lines": matches, "pattern": needle},
                "action": "Authorize a focused work order after confirming runtime behavior with a regression test.",
            })

    findings.append({
        "id": "IMPORT-TIME-MUTABLE-SINGLETONS",
        "classification": "implementation-violation",
        "severity": "P1",
        "rule": "ADR-010 / ADR-011E",
        "evidence": import_time_calls,
        "action": "Separate construction from import and introduce explicit bootstrap in a staged migration.",
    })

    status = git(repo, "status", "--short")
    return {
        "schema_version": 1,
        "tool": {"name": "architecture_inspect", "version": TOOL_VERSION},
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repository": {
            "path": str(repo),
            "commit": git(repo, "rev-parse", "HEAD"),
            "branch": git(repo, "branch", "--show-current"),
            "working_tree": status.splitlines(),
            "python_files_inspected": len(files),
        },
        "checks": {
            "duplicate_classes": {name: paths for name, paths in sorted(duplicate_classes.items()) if len(paths) > 1},
            "registry_contracts": registry_checks,
            "import_time_calls": import_time_calls,
        },
        "findings": findings,
        "limitations": [
            "Static evidence only; runtime behavior, data migrations, and semantic ownership require targeted tests/review.",
            "A finding is not authorization to modify code. Follow the control-plane work-order process.",
        ],
    }


def markdown(report: dict) -> str:
    repo = report["repository"]
    lines = [
        "# QAOS Architecture Inspection", "",
        f"- Generated: {report['generated_at_utc']}",
        f"- Commit: `{repo['commit']}` on `{repo['branch']}`",
        f"- Python files inspected: {repo['python_files_inspected']}",
        f"- Working-tree entries: {len(repo['working_tree'])}", "",
        "## Findings", "",
        "| ID | Severity | Classification | Governing rule |", "| --- | --- | --- | --- |",
    ]
    for item in report["findings"]:
        lines.append(f"| {item['id']} | {item['severity']} | {item['classification']} | {item['rule']} |")
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in report["limitations"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path, help="write JSON evidence report")
    parser.add_argument("--markdown", type=Path, help="write Markdown summary")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    report = inspect(repo)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(markdown(report), encoding="utf-8")
    print(markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
