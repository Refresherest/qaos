# FINDING-015 — Runtime Executive Service Gap

## Status

`RESOLVED — WO-040`

## Evidence

Runtime explicitly registered logger and event services, but create_runtime and
Kernel had no executive input. The explicitly composable ExecutiveManager from
WO-039 could not be retained at the Kernel runtime boundary.

## Resolution

WO-040 adds optional executive forwarding and registration under `executive`,
without importing or selecting a default executive singleton.

## Boundary

Dispatcher, CLI, command registry, handlers, and actual command-to-executive
routing remain outside this work order.
