# WO-071 — Pre-Execution Failure Ownership Decision

## Objective

Obtain an owner decision for FINDING-033 without weakening the established
ExecutionManager lifecycle boundary.

## Architectural Context

WO-059 assigns `start -> complete/fail` to ExecutionManager once execution
begins. OperationalSession creates and persists the Objective before Kernel
invocation and is the only existing boundary that owns both that creation and
the same ObjectiveManager before ExecutionManager is reached.

## Scope

- Compare application-session, Executive-boundary, and pending-preservation
  ownership choices.
- Preserve established execution lifecycle authority in every option.
- Record a recommendation, current state, verification, and handoff.

## Explicit Non-Goals

- No product code, test, lifecycle, pipeline, schema, provider, model,
  credential, Content OS, fallback execution, retry, or deployment change.

## Verification Requirements

- Confirm WO-059 ownership remains authoritative after execution starts.
- Confirm OperationalSession owns objective creation and its shared manager.
- Validate project-state JSON, whitespace, secret, scope, and active-data
  boundaries.

## Stop Condition

Stop after DECISION-REQUEST-008 is published. Implementation requires the
owner's explicit option selection.
