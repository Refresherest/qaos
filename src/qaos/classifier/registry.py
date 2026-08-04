"""
QAOS Intent Classifier Registry
"""

from .classifier import IntentClassifier

classifier = IntentClassifier()

#
# Architecture
#

classifier.register(
    "architecture",
    "validate_architecture",
)

classifier.register(
    "design",
    "design_system",
)

classifier.register(
    "plugin",
    "design_system",
)

#
# Code
#

classifier.register(
    "code",
    "review_code",
)

classifier.register(
    "review",
    "review_code",
)

#
# Executive
#

classifier.register(
    "delegate",
    "delegate_work",
)

classifier.register(
    "objective",
    "analyze_objective",
)