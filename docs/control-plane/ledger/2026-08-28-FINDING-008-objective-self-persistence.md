# FINDING-008 — Objective Self-Persistence

## Status

`RESOLVED — WO-033`

## Evidence

Objective lifecycle methods imported the module-level default
`objective_manager` and called its private `_save`. An Objective created by an
isolated manager could therefore write the wrong workspace.

## Resolution

WO-033 makes Objective transitions state-only and moves persistence ownership
to explicit ObjectiveManager lifecycle methods. Council uses the default
manager explicitly; Content OS uses its injected private manager.

## Boundary

Status values, timestamp behavior, persistence schema, and transition method
names remain unchanged. Transition validation is not introduced.
