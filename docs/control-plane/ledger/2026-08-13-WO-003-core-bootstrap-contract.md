# WO-003: Establish the core bootstrap and composition-root contract

- Status: verified
- Priority: P1
- Owner direction: `CORE_ARCHITECTURE_RECOVERY.md`
- Scope: configuration, Runtime construction, package import behavior, and
  focused characterization tests.
- Non-goals: registry normalization, persistence redesign, mass singleton
  removal, or unrelated domain refactoring.

## Acceptance criteria

1. Record the current import/construction behavior in clean-process tests.
2. Propose a minimal, explicit runtime construction contract from observed code.
3. Obtain/record any decision needed before behavior-changing implementation.
4. Keep the package-import regression suite passing throughout.

## Verification

Clean-process import tests, focused construction tests, full pytest, and the
architecture inspector. The initial implementation decision must be recorded as
a new recovery decision, not backfilled into a draft ADR.

## Result

The owner approved the narrow replacement contract. `create_configuration()`
and `create_runtime()` now construct explicit dependencies; `qaos.core` exposes
no runtime singleton. Status construction is deferred to command execution.
Focused tests and the full suite pass (6 tests), all 44 packages import, and
the inspector count fell from 64 to 61 import-time constructions.
