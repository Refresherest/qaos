"""Bounded Brief -> Reviewed Draft Artifact orchestration."""

from qaos.ai import AIEngine
from qaos.artifacts import ArtifactManager
from qaos.objectives import ObjectiveManager
from qaos.planner import PlannerManager
from qaos.storage import Stores

from .models import Brief, FirstSliceResult, ReviewOutcome, ReviewResult


class BriefToReviewedDraft:
    """Execute the approved first slice against explicitly injected services."""

    def __init__(self, *, stores: Stores, ai_engine: AIEngine, reviewer):
        if not isinstance(stores, Stores):
            raise TypeError("stores must be a Stores instance")

        provider = ai_engine.provider()
        if not getattr(provider, "test_only", False):
            raise ValueError(
                "the first slice requires an explicit test-only provider"
            )

        if not callable(reviewer):
            raise TypeError("reviewer must be callable")

        self._ai_engine = ai_engine
        self._reviewer = reviewer
        self._objectives = ObjectiveManager(stores=stores)
        self._planner = PlannerManager(stores=stores)
        self._artifacts = ArtifactManager(stores=stores)

    def run(self, brief: Brief) -> FirstSliceResult:
        if not isinstance(brief, Brief):
            raise TypeError("brief must be a validated Brief")

        objective = self._objectives.create(
            f"Create {brief.requested_content_type}: {brief.working_title}"
        )
        self._objectives.start(objective)

        plan = self._planner.create(objective)
        task = plan.add_task("Generate one reviewed draft artifact")
        task.start()
        self._planner.save()

        prompt = self._prompt_for(brief)

        try:
            evidence = self._ai_engine.generate_with_evidence(prompt)
        except Exception:
            task.fail()
            self._planner.save()
            self._objectives.fail(objective)
            return FirstSliceResult(
                status="blocked",
                objective=objective,
                artifact=None,
                review=ReviewResult(
                    ReviewOutcome.BLOCKED,
                    ("Draft generation failed.",),
                ),
                evidence=None,
                error="provider_generation_failed",
            )

        artifact = self._artifacts.create(
            title=brief.working_title,
            artifact_type=brief.requested_content_type,
            creator="content-os:first-slice",
            objective=objective.goal,
            content=evidence.output,
        )

        review = self._reviewer(brief, artifact)
        if not isinstance(review, ReviewResult):
            raise TypeError("reviewer must return ReviewResult")

        if review.outcome is ReviewOutcome.ACCEPT:
            task.complete()
            self._planner.save()
            self._objectives.complete(objective)
            status = "completed"
        else:
            task.fail()
            self._planner.save()
            self._objectives.fail(objective)
            status = review.outcome.value.lower()

        return FirstSliceResult(
            status=status,
            objective=objective,
            artifact=artifact,
            review=review,
            evidence=evidence,
        )

    @staticmethod
    def _prompt_for(brief):
        return "\n".join(
            (
                f"Working title: {brief.working_title}",
                f"Purpose: {brief.purpose}",
                f"Intended audience: {brief.intended_audience}",
                f"Core message: {brief.core_message}",
                f"Content type: {brief.requested_content_type}",
                f"Constraints: {brief.constraints}",
            )
        )
