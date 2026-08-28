"""Tests for explicit event-system lifecycle isolation."""

from __future__ import annotations

import pytest

from qaos.events import EventManager
from qaos.events.registry import EventRegistry


def test_explicit_event_managers_isolate_subscribers_and_delivery() -> None:
    first = EventManager(registry=EventRegistry())
    second = EventManager(registry=EventRegistry())
    first_received = []
    second_received = []

    first.subscribe("isolated", first_received.append)
    second.subscribe("isolated", second_received.append)

    first.emit("isolated", {"workspace": "first"})

    assert [event.payload for event in first_received] == [{"workspace": "first"}]
    assert second_received == []
    assert first.handlers("isolated") == [first_received.append]
    assert second.handlers("isolated") == [second_received.append]


def test_default_event_compatibility_and_ambiguous_injection_guard() -> None:
    from qaos.events import event_bus, event_manager
    from qaos.events import registry

    assert event_manager._bus is event_bus
    assert event_manager.all() is registry.EVENTS

    with pytest.raises(ValueError, match="either bus or registry"):
        EventManager(bus=event_bus, registry=EventRegistry())
