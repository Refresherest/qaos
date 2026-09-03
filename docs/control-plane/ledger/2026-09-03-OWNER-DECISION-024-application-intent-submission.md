# OWNER-DECISION-024 — Application Intent Submission

Date: 2026-09-03. Authority: Qaasim April, repository owner.

The owner selects WO-118 Option A, approving all eight rules and the stated
acceptance boundary, including explicit session-to-Executive delegation.

OperationalSession may expose optional python_file_workspace construction and
execute_intent(objective, intent). Submission requires explicit opt-in, the
exact pending session-owned canonical Objective, a validated PythonFileIntent
and no existing Plan. Reject invalid submission before execution-state writes.

The new Executive entry point must reuse the same six-stage pipeline, passing
intent explicitly for one call. PlannerManager creates and persists one Plan
with one identified Task. Existing execution/lifecycle, reflection, learning,
recovery and ExecutionResult contracts remain authoritative. Preserve the
session's pending-failure guard and original exceptions. Never replace Plans.

Kernel and CLI remain unchanged. No direct capability bypass, transient
Objective attributes, duplicate pipeline, arbitrary Task-list API, new intent
types, provider/model selection, shell/Git authority, Content OS expansion,
migration or relaxation of the print-only restriction is approved.

A separate implementation work order may change session, Executive manager,
orchestrator/pipeline, factory wiring, PlannerManager and focused tests plus
records. It must prove the public-session build path, evidence, lifecycle,
preflight rejection, non-replacement, isolation and regression safety.
