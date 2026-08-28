# WO-035 — Knowledge Manager Isolation

## Objective

Give each explicitly stored KnowledgeManager private registry state while
preserving the default module manager and registry compatibility API.

## Architectural Context

KnowledgeManager accepts an explicit Stores collection, but every instance
loads, reads, and persists the same module-level registry. One workspace can
therefore leak knowledge into another workspace's persistence and lookups.

## Approved Contract

1. Knowledge registry state is represented by an instantiable KnowledgeRegistry.
2. A KnowledgeManager with explicit Stores receives a private registry by default.
3. The default manager continues to use the default registry.
4. Existing module-level registry functions continue to target that default.
5. Knowledge schema and public manager methods remain unchanged.

## Scope

- Knowledge registry and KnowledgeManager registry ownership
- Two-workspace isolation and compatibility tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- Do not redesign learning, retrieval, knowledge identity, or categorization.
- Do not change knowledge schema or active data.
- Do not change Content OS, providers, models, or credentials.

## Acceptance Criteria

1. Explicitly stored managers do not share registry state.
2. Each manager persists and resolves only its own knowledge.
3. Default registry compatibility functions retain their behavior.
4. Focused and full verification pass and active data remains unchanged.

## Stop Condition

Stop after knowledge isolation is independently reviewed and published.
