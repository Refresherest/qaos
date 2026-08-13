# BASELINE-003: Remaining import-time construction map

- Timestamp: 2026-08-13 UTC
- Source: `tools/architecture_inspect.py` at the current working tree

## Evidence

The inspector reports 61 import-time constructions. The highest counts are
storage (8), planner (4), then council/executive/learning (3 each). This map is
a triage aid, not a claim that every construction is equally harmful.

## Selected next target

`qaos.container` creates a process-global container but has no repository
consumer. The active recovered core uses the separate instance-based
`qaos.services.container.ServiceContainer`. Retiring the duplicate has a small,
observable blast radius and removes one ambient-state path.
