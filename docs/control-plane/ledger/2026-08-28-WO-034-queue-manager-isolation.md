# WO-034 — Queue Manager Isolation

## Objective

Give each explicitly stored QueueManager private registry state while preserving
the default module manager and registry compatibility API.

## Architectural Context

QueueManager accepts an explicit Stores collection, but every instance clears,
loads, reads, and writes the same module-level queue list. Constructing one
workspace manager can therefore disturb another workspace or the default queue.

## Approved Contract

1. Queue registry state is represented by an instantiable QueueRegistry.
2. A QueueManager with explicit Stores receives a private registry by default.
3. The default QueueManager continues to use the default registry.
4. Existing module-level registry functions continue to target that default.
5. Queue schema, processing behavior, and public QueueManager methods remain.

## Scope

- Queue registry and QueueManager registry ownership
- Two-workspace isolation and compatibility tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- Do not redesign queue processing, workers, tasks, or execution.
- Do not change queue schema, statuses, ordering, or active data.
- Do not change Content OS, providers, models, or credentials.

## Acceptance Criteria

1. Explicitly stored managers do not share or clear registry state.
2. Each manager persists only its own queue items.
3. Default registry compatibility functions retain their behavior.
4. Focused and full verification pass and active data remains unchanged.

## Stop Condition

Stop after queue isolation is independently reviewed and published.
