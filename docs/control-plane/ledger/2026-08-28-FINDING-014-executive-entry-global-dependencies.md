# FINDING-014 — Executive Entry Global Dependencies

## Status

`RESOLVED — WO-039`

## Evidence

ExecutiveOrchestrator and ExecutiveManager directly called imported singleton
services. An explicitly composed pipeline could not be carried through the
public executive manager without monkeypatching globals.

## Resolution

WO-039 adds optional dependency injection through orchestrator and manager,
including the logger boundary, while retaining existing services as defaults.

## Boundary

Kernel/runtime wiring, dispatcher/CLI behavior, pipeline stages, and result
schema remain outside this work order.
