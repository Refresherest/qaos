# FINDING-012 — Event Lifecycle Isolation

## Status

`RESOLVED — WO-037`

## Evidence

Every EventBus and EventManager instance delegated to one module-level
subscriber dictionary. Independently constructed event systems therefore
shared handlers and delivery.

## Resolution

WO-037 introduces an instantiable EventRegistry and explicit registry injection
through EventBus and EventManager. Default objects and compatibility functions
retain the default registry.

## Boundary

Event persistence, asynchronous delivery, ordering, handler exception behavior,
and Council lifecycle semantics are unchanged and not declared correct here.
