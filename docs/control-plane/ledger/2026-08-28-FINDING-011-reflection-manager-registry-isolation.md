# FINDING-011 — Reflection Manager Registry Isolation

## Status

`RESOLVED — WO-036`

## Evidence

ReflectionManager accepted explicit Stores but all instances loaded, queried,
and saved one module-level dictionary. Reflections from one explicit workspace
could therefore be returned and persisted by another.

## Resolution

WO-036 introduces instantiable ReflectionRegistry state. Explicitly stored
managers receive private registries by default; the default manager and
compatibility functions retain the default registry.

## Boundary

Reflection content, pipeline execution, objective identity, schema, and event
delivery are not changed or declared correct by this work order.
