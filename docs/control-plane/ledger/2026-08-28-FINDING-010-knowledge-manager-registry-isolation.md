# FINDING-010 — Knowledge Manager Registry Isolation

## Status

`RESOLVED — WO-035`

## Evidence

KnowledgeManager accepted explicit Stores but all instances loaded, queried,
and saved one module-level dictionary. Knowledge created in one explicit
workspace could therefore be returned and persisted by another.

## Resolution

WO-035 introduces instantiable KnowledgeRegistry state. Explicitly stored
managers receive private registries by default; the default manager and
compatibility functions retain the default registry.

## Boundary

Learning, retrieval, knowledge identity, categorization, and schema are not
changed or declared correct by this work order.
