# BASELINE-002: Core bootstrap and composition boundary

- Timestamp: 2026-08-13 UTC
- Classification: observed implementation evidence
- Governing authority: owner recovery direction; no draft ADR is applied

## Observed behavior

- `qaos.config.configuration` is constructed while importing
  `config/configuration.py`.
- Importing `qaos.core` exposes a process-global `runtime` constructed in
  `core/runtime.py`.
- That runtime is bound to the global configuration and registers the global
  logger and event bus in a process-global service registry.
- The static inventory finds many more import-time singleton constructions
  across the source tree. This makes import order and ambient process state part
  of effective runtime behavior.

## Characterization coverage

`tests/test_core_bootstrap_characterization.py` proves the current Runtime
composition relationship without claiming it is the target architecture. The
test is a safety net for the recovery transition and may be replaced when a
newly approved contract changes the boundary.

## Approved minimal contract

1. Importing a public package exposes types and explicit construction functions
   but does not construct mutable application state.
2. A single explicit `create_runtime(configuration)` composition function owns
   Runtime/service construction.
3. State is passed to components; package modules do not reach into global
   registries to discover it.
4. Compatibility behavior, if any, is time-bounded and separately approved.

Approved by the owner on 2026-08-13. It is deliberately narrow enough to
reconfigure the core first without deciding all registry, persistence, or domain
contracts.
