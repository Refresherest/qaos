# WO-049 — Planning Stage Composition

## Objective

Allow an explicitly composed planning stage to use caller-selected context and
retrieval services without crossing into default workspace state.

## Architectural Context

The executive pipeline already supports an explicit PlannerManager, and the
storage-backed managers already support isolated Stores. The internal planning
chain still selected module services at four boundaries.

## Requirements

1. PlannerManager accepts an explicit PlanGenerator.
2. PlanGenerator accepts an explicit ContextManager.
3. ContextManager accepts explicit retrieval and registry ownership.
4. RetrievalManager and RetrievalEngine accept explicit existing services.
5. Default constructors preserve existing compatibility behavior.

## Scope

- Dependency injection through the existing planning/context/retrieval chain
- Private registry state for explicitly composed ContextManagers
- Focused composition, compatibility, and isolation tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- No planning-task or retrieval-matching changes.
- No ranking, schema, provider, model, credential, or Content OS change.
- No other executive-stage change.

## Verification Requirements

- Prove selected-workspace context affects planning.
- Prove default service selection remains compatible.
- Prove explicit ContextManager registries are isolated.
- Run focused and full regression checks, import sweep, compilation,
  architecture inspection, and active-data comparison.

## Stop Condition

Stop after FINDING-022 is independently reviewed and WO-049 is published.
