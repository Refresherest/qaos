"""End-to-end acceptance tests for the first Content OS slice."""

import pytest

from content_os import (
    Brief,
    BriefToReviewedDraft,
    BriefValidationError,
    ReviewOutcome,
    ReviewResult,
)
from qaos.ai import AIEngine, AIProvider
from qaos.ai.engine import engine as default_engine
from qaos.ai.registry import all_providers
from qaos.storage import create_stores


class DeterministicDraftProvider(AIProvider):
    name = "content-os-deterministic-test"
    test_only = True

    def __init__(self, *, fail=False):
        self.fail = fail
        self.prompts = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        if self.fail:
            raise RuntimeError("synthetic provider failure")
        return "A deterministic reviewed draft."


def accepted_review(brief, artifact):
    assert artifact.title == brief.working_title
    return ReviewResult(ReviewOutcome.ACCEPT, ("Meets the brief.",))


def valid_brief():
    return Brief(
        working_title="First Content OS Draft",
        purpose="Prove the first vertical slice",
        intended_audience="QAOS owner",
        core_message="The bounded workflow is operational",
        requested_content_type="article",
        constraints="Plain text; one concise draft",
    )


def test_success_produces_one_reviewed_artifact_and_completed_objective(tmp_path):
    stores = create_stores(tmp_path)
    provider = DeterministicDraftProvider()
    registry_before = dict(all_providers())
    default_provider_before = default_engine.provider()
    workflow = BriefToReviewedDraft(
        stores=stores,
        ai_engine=AIEngine(provider=provider),
        reviewer=accepted_review,
    )

    result = workflow.run(valid_brief())

    assert result.status == "completed"
    assert result.objective.status == "completed"
    assert result.artifact.content == "A deterministic reviewed draft."
    assert result.review.outcome is ReviewOutcome.ACCEPT
    assert result.evidence.prompt == provider.prompts[0]
    assert result.evidence.output == result.artifact.content
    assert len(provider.prompts) == 1
    assert len(stores.objective_db.load()) == 1
    assert len(stores.plan_db.load()) == 1
    assert stores.plan_db.load()[0]["tasks"][0]["status"] == "completed"
    assert len(stores.artifact_db.load()) == 1
    assert dict(all_providers()) == registry_before
    assert default_engine.provider() is default_provider_before


def test_invalid_brief_fails_before_generation_or_persistence(tmp_path):
    stores = create_stores(tmp_path)
    provider = DeterministicDraftProvider()
    workflow = BriefToReviewedDraft(
        stores=stores,
        ai_engine=AIEngine(provider=provider),
        reviewer=accepted_review,
    )

    with pytest.raises(BriefValidationError):
        workflow.run(
            Brief(
                working_title="",
                purpose="purpose",
                intended_audience="audience",
                core_message="message",
                requested_content_type="article",
                constraints="none",
            )
        )

    assert provider.prompts == []
    assert stores.objective_db.load() == []
    assert stores.plan_db.load() == []
    assert stores.artifact_db.load() == []


def test_provider_failure_records_blocked_result_without_artifact(tmp_path):
    stores = create_stores(tmp_path)
    provider = DeterministicDraftProvider(fail=True)
    workflow = BriefToReviewedDraft(
        stores=stores,
        ai_engine=AIEngine(provider=provider),
        reviewer=accepted_review,
    )

    result = workflow.run(valid_brief())

    assert result.status == "blocked"
    assert result.objective.status == "failed"
    assert result.review.outcome is ReviewOutcome.BLOCKED
    assert result.artifact is None
    assert result.evidence is None
    assert result.error == "provider_generation_failed"
    assert len(provider.prompts) == 1
    assert stores.plan_db.load()[0]["tasks"][0]["status"] == "failed"
    assert stores.artifact_db.load() == []


def test_first_slice_rejects_provider_not_marked_test_only(tmp_path):
    class UnmarkedProvider(AIProvider):
        def generate(self, prompt: str) -> str:
            return prompt

    with pytest.raises(ValueError, match="test-only provider"):
        BriefToReviewedDraft(
            stores=create_stores(tmp_path),
            ai_engine=AIEngine(provider=UnmarkedProvider()),
            reviewer=accepted_review,
        )


@pytest.mark.parametrize(
    ("outcome", "expected_status"),
    (
        (ReviewOutcome.REVISE, "revise"),
        (ReviewOutcome.BLOCKED, "blocked"),
    ),
)
def test_nonaccepted_review_returns_reason_and_does_not_complete_objective(
    tmp_path,
    outcome,
    expected_status,
):
    stores = create_stores(tmp_path)

    def nonaccepted_review(brief, artifact):
        return ReviewResult(outcome, ("A bounded revision is required.",))

    workflow = BriefToReviewedDraft(
        stores=stores,
        ai_engine=AIEngine(provider=DeterministicDraftProvider()),
        reviewer=nonaccepted_review,
    )

    result = workflow.run(valid_brief())

    assert result.status == expected_status
    assert result.objective.status == "failed"
    assert result.review.outcome is outcome
    assert result.review.reasons == ("A bounded revision is required.",)
    assert result.artifact is not None
    assert len(stores.artifact_db.load()) == 1
