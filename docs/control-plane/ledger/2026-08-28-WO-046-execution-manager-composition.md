# WO-046 — Execution Manager Composition

## Objective

Allow ExecutionManager to select an explicit execution-engine registry and
ObjectiveManager persistence service while preserving default behavior.

## Architectural Context

WO-045 made ExecutionEngine collaborators injectable, but ExecutionManager
still resolved the default engine and ObjectiveManager through module globals.
An isolated execution stage therefore remained incomplete.

## Requirements

1. Represent engine state with an instantiable ExecutionRegistry.
2. ExecutionManager accepts explicit registry and objective services.
3. Omitted dependencies use the existing default registry and ObjectiveManager.
4. The default ExecutionEngine remains registered under `default`.
5. Engine execution occurs before objective persistence and returns its report.

## Scope

- Execution registry and ExecutionManager dependency ownership
- Explicit order, missing-engine, and default-compatibility tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- No ExecutionEngine, worker, planner, queue, or objective lifecycle redesign.
- No pipeline, Kernel, CLI, Content OS, provider, model, or credential change.

## Acceptance Criteria

1. Explicit manager executes its registry's default engine then saves through
   its selected ObjectiveManager.
2. An empty explicit registry fails with the existing RuntimeError contract.
3. Default services and module registry compatibility remain.
4. Full verification passes and active data remains unchanged.

## Stop Condition

Stop after ExecutionManager composition is independently reviewed.
