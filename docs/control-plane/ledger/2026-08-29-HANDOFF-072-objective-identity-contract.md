# HANDOFF-072 — Objective Identity Contract

## Work Order

`WO-081`

## Status

`COMPLETE — ACCEPTED WITH NOTES`

## Result

PROPOSAL-006 defines coherent Objective identity generation, registry, and
legacy-loading alternatives. No product code or schema changed.

## Recommendation

Select **Option A — Manager-Injected IDs with Dual Indexes**:

- ObjectiveManager injects and assigns opaque IDs for new records;
- ObjectiveRegistry owns canonical ID lookup plus latest-by-goal compatibility;
- persistence iterates all records without collapsing equal goals;
- legacy missing-ID records remain unassigned and unmodified;
- duplicate non-null IDs fail closed.

## Decision Options

- Option A: manager injection, dual indexes, legacy pass-through — recommended
- Option B: entity self-generation and immediate registry switch
- Option C: deterministic derived identity

## Verification

- Existing construction, registry, persistence, and caller paths: inspected
- Compatibility and duplicate-concept risks: recorded
- Product code and tests: unchanged
- Active data: unchanged
- Reviewer: ACCEPT WITH NOTES

## Next Executable Step

Obtain the owner's selection for DECISION-REQUEST-013. Record the chosen
contract before Objective identity implementation.

## Stop Condition

WO-081 is complete. Stop pending owner decision.
