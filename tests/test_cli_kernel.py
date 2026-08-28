"""Regression tests for the CLI/kernel explicit-entry boundary."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from qaos.config import create_configuration
from qaos.kernel.kernel import Kernel
from qaos.kernel.dispatcher import Dispatcher
from qaos.objectives.objective import Objective


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPOSITORY_ROOT / "src"


def test_kernel_dispatches_arguments_to_explicit_command_handler() -> None:
    captured = []
    dispatcher = Dispatcher(
        commands={
            "run": lambda *args: captured.append(("run", args)),
        }
    )

    assert Kernel(dispatcher=dispatcher).execute("run", "worker") is True
    assert captured == [("run", ("worker",))]


def test_explicit_empty_dispatcher_has_no_default_commands(capsys) -> None:
    dispatcher = Dispatcher(commands={})

    assert dispatcher.dispatch("about") is False
    assert capsys.readouterr().out == "Unknown command: about\n"


def test_default_dispatcher_retains_default_command_mapping() -> None:
    from qaos.commands.registry import COMMANDS

    assert Dispatcher()._commands is COMMANDS


def test_kernel_registers_explicit_executive_service() -> None:
    executive = object()

    kernel = Kernel(executive=executive)

    assert kernel.runtime.get("executive") is executive


def test_kernel_executes_canonical_objective_through_runtime_service(tmp_path) -> None:
    objective = Objective("execute explicit objective")
    expected_result = object()
    received = []

    class Executive:
        def execute(self, value):
            received.append(value)
            return expected_result

    kernel = Kernel(
        configuration=create_configuration(tmp_path),
        executive=Executive(),
    )

    assert kernel.execute_objective(objective) is expected_result
    assert received == [objective]
    assert not (tmp_path / "objectives.json").exists()


def test_kernel_rejects_noncanonical_objective() -> None:
    kernel = Kernel(executive=object())

    with pytest.raises(TypeError, match="canonical QAOS Objective"):
        kernel.execute_objective("raw goal")


def test_kernel_requires_registered_executive_for_objective() -> None:
    kernel = Kernel()

    with pytest.raises(RuntimeError, match="executive service is not registered"):
        kernel.execute_objective(Objective("missing service"))


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
