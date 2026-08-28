# WO-045 — Execution Engine Dependency Injection

## Objective

Allow ExecutionEngine to use explicitly selected PlannerManager and QueueManager
collaborators while preserving its default execution behavior.

## Architectural Context

ExecutivePipeline is injectable, but an explicitly selected ExecutionEngine
still directly calls module-level planner and queue managers. This breaks the
isolated workspace chain at the execution stage.

## Requirements

1. ExecutionEngine accepts optional keyword-only planner and queue dependencies.
2. Omitted dependencies resolve to the existing default managers.
3. Plan lookup/generation, task queueing, queue processing, and planner save order remain.
4. ExecutionReport completion, failure propagation, and stage ownership remain.

## Scope

- ExecutionEngine planner and queue dependency selection
- Explicit-composition and default-compatibility tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- No worker selection or QueueManager redesign.
- No ExecutionManager registry or ObjectiveManager ownership change.
- No pipeline, CLI, Content OS, provider, model, or credential change.

## Acceptance Criteria

1. Explicit planner and queue collaborators execute in the existing order.
2. Execution produces one successful report without reflection ownership.
3. Default constructor retains existing managers.
4. Full verification passes and active data remains unchanged.

## Stop Condition

Stop after ExecutionEngine dependency injection is independently reviewed.
