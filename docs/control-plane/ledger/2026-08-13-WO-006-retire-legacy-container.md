# WO-006: Retire the duplicate legacy container package

- Status: verified
- Priority: P1
- Authority: RECOVERY-DECISION-001; BASELINE-003 evidence
- Scope: `src/qaos/container` removal and focused regression coverage.
- Non-goals: changing the instance-based services container or global manager
  registries.

## Acceptance criteria

1. `qaos.container` is not importable.
2. No source references it.
3. The explicit core runtime and full suite continue to pass.

## Result

The duplicate container files and namespace directory were removed. A focused
test proves `qaos.container` has no import spec; no source references remain.
The full suite passes (10 tests), and inspection count fell from 61 to 60.
