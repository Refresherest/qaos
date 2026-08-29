# PROPOSAL-005 — Execution-Attempt Identity

## Evidence Summary

- OperationalSession creates a new Objective for each `execute_goal` call.
- Objective already owns pending/running/completed/failed state and timestamps.
- ExecutionManager owns that Objective's execution lifecycle.
- Plan and QueueItem currently retain only the Objective goal string.
- ObjectiveManager and PlannerManager registries are keyed by goal text.
- JSON records contain no opaque identity or attempt/batch field.
- No active canonical ID generator or ExecutionAttempt domain exists.

## Design Requirements

1. One operational invocation must have one canonical opaque identity.
2. Plan and QueueItem records must reference that identity without becoming its
   source of truth.
3. Identity must remain provider-neutral and stable across reload.
4. Repeated equal goal text must not collapse distinct invocations.
5. Legacy records must not be correlated by guesswork.
6. Recovery selection must remain outside this identity-only design.

## Recommended Shape

Treat canonical Objective identity as execution-attempt identity:

- Objective receives an immutable opaque `objective_id` at creation.
- ObjectiveManager becomes the source of truth for that identity.
- OperationalSession continues creating one Objective per invocation.
- Plan stores `objective_id` alongside its compatibility objective text.
- QueueItem stores `objective_id` alongside its compatibility objective text.
- Execution boundaries pass the Objective or its ID explicitly; provider and
  model identifiers never influence it.
- ID creation uses an injectable generator with a deterministic test double;
  the default may produce UUID-compatible opaque strings.

## Compatibility Boundary

- Existing public goal-based lookup may remain as an explicitly defined
  compatibility projection, not canonical identity.
- Legacy JSON records without `objective_id` load with identity absent.
- QAOS must not infer legacy identity by matching goal text, timestamps, list
  order, or Task descriptions.
- Legacy unassigned queue work is not eligible for identity-based recovery.
- Any registry-key transition and write-forward behavior require separate
  implementation and migration decisions.

## Lifecycle Boundary

This design implies one Objective lifecycle represents one operational
invocation. Re-executing the same Objective instance would require a separate
future decision; normal OperationalSession behavior already creates a fresh
Objective for each call.

## Recovery Boundary

Identity enables selection but does not authorize recovery. A future recovery
API must explicitly select one failed `objective_id`, validate its state, and
define whether it continues pending work or retries failed work.
