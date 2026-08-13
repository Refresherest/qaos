"""Guard against reintroducing the retired duplicate container package."""

from importlib.util import find_spec


def test_legacy_container_package_is_not_importable() -> None:
    assert find_spec("qaos.container") is None
