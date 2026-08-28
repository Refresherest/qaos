"""Tests for explicit classifier-stage composition."""

from __future__ import annotations

import qaos.classifier.manager as manager_module
from qaos.classifier import ClassifierManager, IntentClassifier
from qaos.classifier.registry import create_default_classifier
from qaos.objectives.objective import Objective


def test_classifier_manager_uses_selected_classifier() -> None:
    classifier = IntentClassifier()
    classifier.register("isolated", "selected_skill")
    manager = ClassifierManager(classifier_service=classifier)

    assert manager.classify(Objective("isolated objective")) == "selected_skill"
    assert manager.classify(Objective("architecture objective")) is None


def test_classifier_manager_default_retains_default_classifier(monkeypatch) -> None:
    default_classifier = object()
    monkeypatch.setattr(manager_module, "classifier", default_classifier)

    manager = ClassifierManager()

    assert manager._classifier is default_classifier


def test_default_classifier_uses_canonical_general_fallback() -> None:
    classifier = create_default_classifier()

    assert classifier.classify(Objective("ship the next useful thing")) == (
        "general_objective"
    )
    assert classifier.classify(Objective("review this change")) == "review_code"


def test_custom_classifier_fallback_is_explicit() -> None:
    default_custom = IntentClassifier()
    selected_custom = IntentClassifier(fallback="selected_fallback")

    assert default_custom.classify(Objective("unmatched")) is None
    assert selected_custom.classify(Objective("unmatched")) == "selected_fallback"
