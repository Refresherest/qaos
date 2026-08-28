"""Content OS domain values for the first vertical slice."""

from dataclasses import dataclass
from enum import Enum

from qaos.ai import GenerationEvidence
from qaos.artifacts import Artifact
from qaos.objectives import Objective


class BriefValidationError(ValueError):
    """Raised when a Content OS brief is incomplete."""


@dataclass(frozen=True)
class Brief:
    working_title: str
    purpose: str
    intended_audience: str
    core_message: str
    requested_content_type: str
    constraints: str

    def __post_init__(self):
        for field_name, value in self.__dict__.items():
            if not isinstance(value, str) or not value.strip():
                raise BriefValidationError(
                    f"{field_name} must be non-empty plain text"
                )


class ReviewOutcome(str, Enum):
    ACCEPT = "ACCEPT"
    REVISE = "REVISE"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class ReviewResult:
    outcome: ReviewOutcome
    reasons: tuple[str, ...] = ()

    def __post_init__(self):
        if not isinstance(self.outcome, ReviewOutcome):
            raise TypeError("outcome must be a ReviewOutcome")

        if self.outcome is not ReviewOutcome.ACCEPT and not self.reasons:
            raise ValueError("REVISE and BLOCKED outcomes require reasons")

        if any(
            not isinstance(reason, str) or not reason.strip()
            for reason in self.reasons
        ):
            raise ValueError("review reasons must be non-empty text")


@dataclass(frozen=True)
class FirstSliceResult:
    status: str
    objective: Objective | None
    artifact: Artifact | None
    review: ReviewResult
    evidence: GenerationEvidence | None
    error: str | None = None
