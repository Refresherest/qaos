# WO-002: Restore exactly-once reflection and learning ownership

- Status: verified
- Priority: P0
- Authority: ADR-002, ADR-011I, ADR-011J
- Scope: Executive pipeline, execution engine/manager, and focused tests.
- Non-goals: registry standardization, serialization migration, durable-store redesign.
- Linked finding: FINDING-002

## Acceptance criteria

1. Execution produces one `ExecutionReport` and no reflection or learning artifact.
2. Reflection creates one reflection from that report; Learning consumes it once.
3. An end-to-end fixture proves one artifact per stage and no duplicate durable write.
4. The focused tests, import sweep, and architecture inspector are recorded.

## Verification

Create a deterministic fixture with spy/in-memory ports; do not use current
module-global managers as test evidence for the target design.

## Result

Completed 2026-08-13 UTC. The focused test fixture injects stage doubles into
the pipeline and confirms the exact order: classify, delegate, plan, execute,
reflect, learn, persist. A separate execution test confirms it returns only an
execution report. The full test suite passes (4 tests).
