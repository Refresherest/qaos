# WO-051 — Council Stage Composition

## Objective

Allow an explicitly composed council stage to retain caller-selected council,
objective, and queue ownership without crossing into module state.

## Architectural Context

ExecutivePipeline already accepts a CouncilManager and storage-backed Objective
and Queue managers already support isolated Stores. CouncilManager and Delegator
still selected module collaborators internally.

## Requirements

1. CouncilRegistry is instantiable while compatibility functions retain the default.
2. Delegator accepts explicit council registry and ObjectiveManager services.
3. CouncilManager accepts explicit registry, Delegator, and QueueManager services.
4. Delegation keeps the established CTO-first selection and queue output contract.
5. Default constructors preserve existing compatibility behavior.

## Scope

- Council registry lifecycle
- CouncilManager and Delegator dependency injection
- Explicit workspace, default compatibility, and registry-isolation tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- No member, routing, assignment, queue-processing, or event-lifecycle changes.
- No schema, provider, model, credential, Content OS, or other stage change.

## Verification Requirements

- Prove explicit objective assignment and queue persistence use selected Stores.
- Prove explicit council registries are isolated.
- Prove default service compatibility.
- Run focused and full regression checks, import sweep, compilation,
  architecture inspection, and active-data comparison.

## Stop Condition

Stop after FINDING-024 is independently reviewed and WO-051 is published.
