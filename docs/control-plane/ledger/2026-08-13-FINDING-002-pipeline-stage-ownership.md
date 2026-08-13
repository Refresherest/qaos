# FINDING-002: Reflection and learning have overlapping producers

- Status: resolved
- Severity: P0
- Classification: implementation-violation
- Governing authority: ADR-002; ADR-011I; ADR-011J
- Baseline: `f729c1b2ec24c28229d67d1135996ab365902534`, `main`

## Evidence

- `src/qaos/execution/engine.py:91` constructs a reflection.
- `src/qaos/execution/manager.py:55` learns from a reflection.
- `src/qaos/executive/pipeline.py:71` reflects and `:83` learns again.

This directly conflicts with the sole-producer/stage-purity rules: Execution
produces `ExecutionReport`; Reflection produces `Reflection`; Learning consumes
that reflection once. The inspector also records the static evidence.

## Required response

WO-002 removed reflection construction from `ExecutionEngine` and learning from
`ExecutionManager`. The executive pipeline remains the sole coordinator. Two
deterministic stage-boundary tests pass; a static scan confirms execution has
no reflection or learning calls. See VERIFICATION-003.
