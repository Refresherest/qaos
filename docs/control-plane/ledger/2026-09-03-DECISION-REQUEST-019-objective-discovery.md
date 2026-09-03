# DECISION-REQUEST-019 — Objective Discovery

## Status

OPEN — OWNER DECISION REQUIRED

## Options

### A — Read-Only Workspace Listing (Recommended)

Adopt PROPOSAL-012: objectives --workspace lists every Objective ID, status and
goal without mutation. Makes IDs discoverable for explicit recovery while
keeping eligibility validation inside recovery. Legacy IDs remain unidentified.

### B — Report IDs During Execution Only

Assess adding Objective IDs to execution success/failure output instead of a
listing. Helps future invocations but does not discover already persisted
attempts and changes the existing execution reporting contract.

### C — Defer Discovery

Keep recovery limited to callers who already know IDs. Avoids another public
command but leaves the current operator usability gap.

## Recommendation

Select A. Complete read-only enumeration uses existing canonical manager
contracts without introducing new identity or execution ownership. Selection
must precede implementation; no UI, migration or retry authority is implied.
