"""Provider-neutral evidence produced by one AI generation call."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GenerationEvidence:
    """Immutable request/output evidence for one provider invocation."""

    prompt: str
    output: str
