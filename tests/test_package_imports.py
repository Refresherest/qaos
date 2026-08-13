"""Regression tests for public-package import contracts."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPOSITORY_ROOT / "src"


@pytest.mark.parametrize("package", ["qaos.config", "qaos.core"])
def test_public_package_imports_in_clean_process(package: str) -> None:
    """A public package must import without depending on prior import order."""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(SOURCE_ROOT)
    result = subprocess.run(
        [sys.executable, "-c", f"import {package}"],
        cwd=REPOSITORY_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
