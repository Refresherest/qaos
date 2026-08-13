"""Guard against reintroducing the dormant parallel persistence framework."""

from importlib.util import find_spec


def test_legacy_persistence_package_is_not_importable() -> None:
    assert find_spec("qaos.persistence") is None
