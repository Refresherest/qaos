"""Focused tests for explicitly injected deterministic generation."""

from dataclasses import FrozenInstanceError

import pytest

from qaos.ai import AIEngine, AIProvider, GenerationEvidence
from qaos.ai.engine import engine as default_engine
from qaos.ai.registry import all_providers


class DeterministicProvider(AIProvider):
    name = "unregistered-deterministic-test-provider"

    def __init__(self):
        self.prompts = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return f"deterministic::{prompt}"


def test_default_engine_resolves_builtin_mock_provider() -> None:
    engine = AIEngine()

    evidence = engine.generate_with_evidence("default request")

    assert engine.provider().name == "mock"
    assert "mock" in all_providers()
    assert "base" not in all_providers()
    assert evidence == GenerationEvidence(
        prompt="default request",
        output="[MOCK AI] Response to: default request",
    )


def test_injected_provider_returns_immutable_generation_evidence() -> None:
    registry_before = dict(all_providers())
    default_provider_before = default_engine.provider()
    provider = DeterministicProvider()
    engine = AIEngine(provider=provider)

    evidence = engine.generate_with_evidence("exact request")

    assert evidence == GenerationEvidence(
        prompt="exact request",
        output="deterministic::exact request",
    )
    assert provider.prompts == ["exact request"]
    assert dict(all_providers()) == registry_before
    assert default_engine.provider() is default_provider_before

    with pytest.raises(FrozenInstanceError):
        evidence.output = "changed"


def test_generate_compatibility_and_named_provider_selection() -> None:
    provider = DeterministicProvider()
    engine = AIEngine(provider=provider)

    assert engine.generate("compatible request") == (
        "deterministic::compatible request"
    )
    assert provider.prompts == ["compatible request"]

    registered_provider = next(iter(all_providers().values()))
    engine.use(registered_provider.name)

    assert engine.provider() is registered_provider
    assert engine.generate("named request") == (
        "[MOCK AI] Response to: named request"
    )
