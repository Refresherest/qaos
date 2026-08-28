"""
QAOS Intent Classifier Registry
"""

from .classifier import IntentClassifier


def create_default_classifier():
    """Create an isolated classifier with the canonical built-in rules."""
    service = IntentClassifier(fallback="general_objective")

    for keyword, classification in (
        ("architecture", "validate_architecture"),
        ("design", "design_system"),
        ("plugin", "design_system"),
        ("code", "review_code"),
        ("review", "review_code"),
        ("delegate", "delegate_work"),
        ("objective", "analyze_objective"),
    ):
        service.register(keyword, classification)

    return service


classifier = create_default_classifier()
