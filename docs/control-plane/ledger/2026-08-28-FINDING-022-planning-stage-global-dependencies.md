# FINDING-022 — Planning Stage Global Dependencies

## Status

`RESOLVED — WO-049`

## Evidence

PlannerManager accepted isolated Stores but always called the module PlanGenerator.
That generator called the module ContextManager, whose retrieval path used module
RetrievalManager, RetrievalEngine, and active-data managers. An explicitly
composed executive pipeline could therefore read context from the wrong workspace.

## Resolution

WO-049 adds explicit dependency selection through the existing planning,
context, and retrieval chain. Explicit ContextManagers own private in-memory
registries while default constructors retain compatibility services.

## Boundary

Planning rules, retrieval matching, ranking, persistence schemas, and other
executive stages are unchanged and not declared correct by this work order.
