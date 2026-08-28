# WO-037 — Event Lifecycle Isolation

## Objective

Provide explicit, isolated event subscriber lifecycles while preserving the
default event bus, manager, registry functions, and Council subscriptions.

## Architectural Context

EventBus and EventManager are instantiable, but all instances use one
module-level subscriber dictionary. A test or workspace cannot construct an
independent event lifecycle, and handlers can receive another lifecycle's events.

## Approved Contract

1. Subscriber state is represented by an instantiable EventRegistry.
2. EventBus accepts an explicit registry and routes only through that registry.
3. EventManager accepts either an explicit bus or registry, never both.
4. Default constructors and module compatibility APIs retain the default state.
5. Event payload, synchronous delivery, ordering, and exception behavior remain.

## Scope

- Event registry, bus, and manager dependency ownership
- Explicit delivery-isolation and compatibility tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- Do not persist events or use the unused event storage boundary.
- Do not change asynchronous behavior, delivery order, or exception handling.
- Do not change Council lifecycle behavior, Content OS, providers, or credentials.

## Acceptance Criteria

1. Two explicitly configured event managers do not share handlers or delivery.
2. Default event manager and bus retain the default registry and subscriptions.
3. Ambiguous bus-plus-registry injection fails explicitly.
4. Full verification passes and active data remains unchanged.

## Stop Condition

Stop after event lifecycle isolation is independently reviewed and published.
