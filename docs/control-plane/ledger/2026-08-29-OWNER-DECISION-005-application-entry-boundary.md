# OWNER-DECISION-005 — Application Entry Boundary

## Status

`ACCEPTED`

## Decision

The owner selected **Option A — Operational Application Session** from
DECISION-REQUEST-005.

QAOS may add one provider-neutral application boundary that owns an explicit
Stores workspace, a shared ObjectiveManager, the composed Executive, and a
Kernel. Its public operation may accept a validated goal, create the canonical
Objective through that manager, and return the existing ExecutionResult.

This decision does not authorize CLI integration, Content OS integration,
provider/model selection, credentials, fallback, retry, deployment, remote
execution, or schema changes.
