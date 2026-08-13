"""Guard against reintroducing the retired duplicate runtime package."""

from importlib.util import find_spec


def test_legacy_runtime_package_is_not_importable() -> None:
    assert find_spec("qaos.runtime") is None
