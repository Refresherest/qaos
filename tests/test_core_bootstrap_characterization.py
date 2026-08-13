"""Tests for the explicit QAOS core construction boundary."""

from qaos.config import create_configuration
from qaos.core import create_runtime


def test_runtime_composes_only_explicit_dependencies(tmp_path) -> None:
    configuration = create_configuration(tmp_path)
    logger = object()
    event_bus = object()

    runtime = create_runtime(configuration, logger=logger, event_bus=event_bus)

    assert runtime.config is configuration
    assert runtime.get("logger") is logger
    assert runtime.get("events") is event_bus


def test_core_public_package_exposes_no_runtime_singleton() -> None:
    import qaos.core as core
    import qaos.core.runtime as runtime_module

    assert hasattr(core, "create_runtime")
    assert not hasattr(runtime_module, "runtime")
