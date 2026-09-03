# DECISION-REQUEST-020 — Objective ID Reporting

## Status

OPEN — OWNER DECISION REQUIRED

## Options

### A — Create Then Execute in OperationalSession (Recommended)

Adopt PROPOSAL-013. Expose the existing creation and execution steps explicitly,
keep execute_goal compatible, and print the ID before CLI execution. Failure
keeps its original internal exception and yields an immediately usable ID.

### B — Report ID on Success Only

Add the ID to the existing success summary without changing OperationalSession.
Smallest change, but it does not solve the failure-to-recovery usability gap.

### C — Require Listing After Failure

Leave objective output unchanged and instruct operators to run objectives after
failure. Avoids API changes but requires correlating among possibly repeated
goals and concurrent attempts; no automated selection may be inferred.

## Recommendation

Select A. It exposes canonical state before execution rather than reconstructing
identity afterward. Implementation requires a separate work order.
