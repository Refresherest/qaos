"""Regression tests for the CLI/kernel explicit-entry boundary."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from qaos.kernel.kernel import Kernel
import qaos.kernel.kernel as kernel_module


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPOSITORY_ROOT / "src"


def test_kernel_dispatches_arguments_to_command_handler(monkeypatch) -> None:
    captured = []
    monkeypatch.setattr(kernel_module.Dispatcher, "dispatch", lambda self, name, *args: captured.append((name, args)) or True)

    assert Kernel().execute("run", "worker") is True
    assert captured == [("run", ("worker",))]


def test_kernel_registers_explicit_executive_service() -> None:
    executive = object()

    kernel = Kernel(executive=executive)

    assert kernel.runtime.get("executive") is executive


def test_cli_help_runs_without_legacy_runtime_bootstrap() -> None:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(SOURCE_ROOT)
    result = subprocess.run(
        [sys.executable, "-m", "qaos.main"],
        cwd=REPOSITORY_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "QAOS Command Line Interface" in result.stdout
    assert "Logger initialized" not in result.stdout
