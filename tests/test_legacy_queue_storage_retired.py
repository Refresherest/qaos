"""Guard against reintroducing the dead queue storage construction path."""

from importlib.util import find_spec


def test_dead_queue_storage_module_is_not_importable() -> None:
    assert find_spec("qaos.queue.queue_db") is None
