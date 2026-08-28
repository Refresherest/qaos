# WO-039 — Executive Entry-Chain Composition

## Objective

Carry an explicitly selected ExecutivePipeline through ExecutiveOrchestrator
and ExecutiveManager while preserving the default executive entry chain.

## Architectural Context

WO-038 made pipeline stages injectable, but ExecutiveOrchestrator still called
the module pipeline and ExecutiveManager still called the module orchestrator
and logger. Explicit pipeline composition could not reach the public manager.

## Approved Contract

1. ExecutiveOrchestrator accepts an optional explicit pipeline.
2. ExecutiveManager accepts optional explicit orchestrator and logger services.
3. Omitted dependencies resolve to existing default services.
4. Result creation, completion, exception propagation, and logging remain.

## Scope

- ExecutiveOrchestrator and ExecutiveManager dependency selection
- Explicit success, failure, and default-compatibility tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- Do not change the six pipeline stages or result schema.
- Do not change Kernel, runtime, dispatcher, CLI, or service registration.
- Do not implement a second Content OS slice or change providers or credentials.

## Acceptance Criteria

1. An explicit manager executes an explicit pipeline exactly once via its orchestrator.
2. Successful execution completes and returns the existing ExecutionResult.
3. Pipeline failures continue to propagate.
4. Default constructors retain existing services; full verification passes.

## Stop Condition

Stop after executive entry-chain composition is independently reviewed and published.
