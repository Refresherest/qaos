# WO-044 — Kernel Objective Invocation

## Objective

Implement OWNER-DECISION-003 Option A as a programmatic
`Kernel.execute_objective(objective)` boundary.

## Architectural Context

Runtime retains an explicit executive service, but Kernel has no approved
operation that invokes it. OWNER-DECISION-003 authorizes canonical Objective
input without changing CLI, dispatcher, or persistence ownership.

## Requirements

1. Accept only an existing canonical QAOS Objective.
2. Resolve the Runtime service registered under `executive`.
3. Fail explicitly when input is invalid or the service is absent.
4. Call the service once and return its ExecutionResult unchanged.
5. Do not create or persist an Objective implicitly.
6. Preserve `Kernel.execute`, Dispatcher, CLI, and `run <member>` behavior.

## Scope

- Kernel programmatic objective invocation
- Type, missing-service, success, persistence, and compatibility tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- No new or changed CLI command.
- No raw-goal conversion or implicit ObjectiveManager selection.
- No pipeline, executive, dispatcher, persistence, or Content OS redesign.
- No provider, model, or credential change.

## Acceptance Criteria

1. Canonical Objective input reaches the exact Runtime executive once.
2. The exact service result is returned.
3. Invalid input raises TypeError and missing service raises RuntimeError.
4. No objective persistence occurs and legacy command tests remain green.
5. Full verification passes and active data is unchanged.

## Stop Condition

Stop after Option A is independently reviewed and published.
