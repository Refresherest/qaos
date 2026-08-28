# HANDOFF-033 — Executive Invocation Boundary Decision

## Work Order

`WO-042`

## Status

`COMPLETE — ACCEPT; OWNER DECISION PENDING`

## Result

FINDING-017 records that Runtime executive registration is not yet an invocation
contract and that legacy `run <member>` cannot be silently repurposed.
DECISION-REQUEST-003 presents three options and recommends Option A: a distinct
programmatic `Kernel.execute_objective(objective)` boundary.

## Verification

- Full baseline: 57 tests passed
- Product code and tests: unchanged
- Active data: unchanged
- Project-state JSON, secrets, and whitespace: passed
- Reviewer: `ACCEPT`

## Intentionally Untouched

- Kernel, Runtime, Dispatcher, CLI, commands, Council, Objective, and Executive code
- Content OS slice scope and future slices
- Providers, models, credentials, and unrelated working-tree changes

## Next Executable Step

The owner selects DECISION-REQUEST-003 Option A, B, or C. If Option A is
approved, record the decision and issue a separate bounded implementation order.

## Stop Condition

WO-042 is complete. Stop pending owner selection.
