# WO-062 — Application Entry Boundary Decision

## Objective

Identify the first application-facing consumer of `create_executive` and obtain
an owner decision before authorizing raw-goal or CLI behavior.

## Architectural Context

WO-061 provides the reusable Executive graph. Kernel accepts only canonical
Objectives, and correct lifecycle persistence requires the creating
ObjectiveManager to be shared with the Executive. No production boundary yet
owns Stores, objective creation, Executive composition, and Kernel invocation
as one application lifecycle.

## Scope

- Inspect Kernel, Runtime, CLI, Executive factory, and Content OS contracts.
- Record bounded application-entry alternatives and a recommendation.
- Update current state and handoff records.

## Explicit Non-Goals

- No product code, public API, test, CLI, raw-goal, Content OS, provider, model,
  credential, fallback, retry, deployment, or schema change.

## Verification Requirements

- Confirm the current CLI only dispatches registered legacy commands.
- Confirm Kernel rejects raw goals and requires a canonical Objective.
- Confirm Content OS remains a separate, already-verified workflow.
- Validate project-state JSON, whitespace, secret, scope, and active-data
  boundaries.

## Stop Condition

Stop after DECISION-REQUEST-005 is published. Implementation requires the
owner's explicit option selection.
