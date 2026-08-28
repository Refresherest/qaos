# FINDING-013 — Executive Pipeline Global Dependencies

## Status

`RESOLVED — WO-038`

## Evidence

ExecutivePipeline directly referenced six module-level managers. Constructing a
pipeline did not provide a supported way to select isolated stage lifecycles,
and tests required monkeypatching module globals.

## Resolution

WO-038 adds keyword-only stage dependency injection with the existing managers
as compatibility defaults. Exact stage order and exactly-once behavior are
proven using explicitly supplied dependencies.

## Boundary

ExecutiveOrchestrator, ExecutiveManager, Kernel/runtime composition, and stage
domain behavior remain outside this work order.
