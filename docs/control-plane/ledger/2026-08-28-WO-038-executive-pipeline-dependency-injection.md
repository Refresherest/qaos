# WO-038 — Executive Pipeline Dependency Injection

## Objective

Allow the canonical six-stage ExecutivePipeline to run with explicitly selected
stage managers while preserving its existing default construction and ordering.

## Architectural Context

The pipeline is instantiable but directly calls six module-level managers.
QAOS now has isolated manager lifecycles, yet they cannot be composed into the
canonical classification-to-learning sequence without monkeypatching globals.

## Approved Contract

1. ExecutivePipeline accepts optional keyword-only dependencies for all stages.
2. Omitted dependencies resolve to the existing default managers.
3. Stage order and exactly-once ownership remain classify, delegate, plan,
   execute, reflect, learn.
4. Result fields and return behavior remain unchanged.

## Scope

- ExecutivePipeline dependency selection
- Explicit-injection and default-compatibility tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- Do not redesign stages or their domain contracts.
- Do not change ExecutiveOrchestrator, ExecutiveManager, Kernel, or runtime.
- Do not implement a second Content OS slice or change providers or credentials.

## Acceptance Criteria

1. Six explicitly injected dependencies execute once in canonical order.
2. The default constructor captures the existing default managers.
3. Existing execution-result semantics and full regression suite remain green.
4. Active data remains unchanged.

## Stop Condition

Stop after pipeline dependency injection is independently reviewed and published.
