# WO-005: Retire the duplicate legacy runtime package

- Status: verified
- Priority: P0
- Authority: RECOVERY-DECISION-001
- Scope: `src/qaos/runtime` removal and focused regression coverage.

## Evidence

No repository code imports `qaos.runtime`. Its `Runtime` duplicates the core
runtime and imports `configuration` after that singleton was removed; Python
resolves the name to the configuration module rather than a Configuration
instance. The resulting construction is semantically invalid.

## Acceptance criteria

1. `qaos.runtime` is not importable.
2. No repository source imports it.
3. The explicit `qaos.core` construction path and all existing tests continue
   to work.

## Result

The legacy runtime files and empty namespace directory were removed. A focused
test proves `qaos.runtime` has no import spec. No source references remain and
the full suite passes (9 tests).
