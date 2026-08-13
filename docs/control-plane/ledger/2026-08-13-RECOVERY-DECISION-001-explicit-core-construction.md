# RECOVERY-DECISION-001: Explicit core construction boundary

- Status: accepted by owner
- Date: 2026-08-13
- Scope: `qaos.config`, `qaos.core`, and status-service construction

## Decision

Public core/config packages expose constructors and factories, not constructed
mutable application state. `create_configuration()` creates a configuration;
`create_runtime(configuration, ...)` composes a runtime from explicit
dependencies. The status command constructs its dependencies when executed.

## Evidence and verification

The change removes the config/runtime/status import-time constructions. Six
tests pass, the isolated 44-package import sweep passes, and static import-time
construction count decreased from 64 to 61.

## Deliberate boundary

This does not authorize or imply a repository-wide singleton migration. Each
remaining global construction requires separate evidence and a scoped recovery
decision.
