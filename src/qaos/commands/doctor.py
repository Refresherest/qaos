import os
import platform
from pathlib import Path


def check(name, condition):
    status = "✓" if condition else "✗"
    print(f"{status} {name}")


def execute():
    print("=" * 50)
    print("QAOS Development Environment Check")
    print("=" * 50)

    project_root = Path.cwd()

    print(f"Python Version : {platform.python_version()}")
    print()

    check("Virtual environment active", os.getenv("VIRTUAL_ENV") is not None)
    check("Git repository", (project_root / ".git").exists())
    check("docs folder", (project_root / "docs").exists())
    check("src folder", (project_root / "src").exists())
    check("pyproject.toml", (project_root / "pyproject.toml").exists())
    check("README.md", (project_root / "README.md").exists())