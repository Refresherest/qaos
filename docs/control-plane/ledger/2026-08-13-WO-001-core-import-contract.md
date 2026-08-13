# WO-001: Repair the canonical configuration package contract

- Status: verified
- Priority: P0
- Authority: ADR-004/004A, ADR-005/005A, ADR-010, ADR-011B
- Scope: `qaos.config`, `qaos.core`, and focused import tests only.
- Non-goals: global bootstrap redesign; broad package-export normalization.
- Linked finding: FINDING-001

## Acceptance criteria

1. All QAOS packages import independently in a clean process.
2. The public configuration name is canonical and documented; any compatibility
   bridge satisfies ADR-004A or is rejected by an owner decision.
3. The test suite contains an isolated package-import regression test.
4. Compile, package import sweep, and pytest run with recorded results.

## Verification

`PYTHONPATH=src python -c "import qaos.core"` and a package-import test command.

## Result

Completed 2026-08-13 UTC. `Runtime` now imports the existing canonical
`configuration` export. The repository declares `pytest>=9` in the `test`
optional dependency group. Focused and full pytest runs passed (2 tests), and
an isolated 44-package import sweep completed successfully.
