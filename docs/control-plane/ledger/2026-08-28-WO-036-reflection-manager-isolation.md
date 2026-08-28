# WO-036 — Reflection Manager Isolation

## Objective

Give each explicitly stored ReflectionManager private registry state while
preserving the default manager, registry API, and objective identity behavior.

## Architectural Context

ReflectionManager accepts an explicit Stores collection, but every instance
loads, queries, and persists the same module-level registry. One workspace can
therefore leak reflections into another workspace's persistence and lookups.

## Approved Contract

1. Reflection state is represented by an instantiable ReflectionRegistry.
2. A ReflectionManager with explicit Stores receives a private registry by default.
3. The default manager continues to use the default registry.
4. Module registry functions continue to target that default.
5. Objective-object and string keys, schema, and public methods remain unchanged.

## Scope

- Reflection registry and ReflectionManager registry ownership
- Two-workspace isolation and compatibility tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- Do not redesign reflection content, pipeline execution, or objective identity.
- Do not change reflection schema or active data.
- Do not change events, Content OS, providers, models, or credentials.

## Acceptance Criteria

1. Explicitly stored managers do not share registry state.
2. Each manager persists and resolves only its own reflections.
3. Default registry compatibility and identity behavior remain.
4. Focused and full verification pass and active data remains unchanged.

## Stop Condition

Stop after reflection isolation is independently reviewed and published.
