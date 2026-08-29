# DECISION-REQUEST-017 — Application Recovery Boundary

## Status

`RESOLVED — OWNER-DECISION-017 selected Option A`

## Decision Required

Choose whether and where the verified internal Objective recovery operation
becomes application-facing.

## Options

### Option A — OperationalSession Boundary (Recommended)

Add `OperationalSession.recover_objective(objective_id)`. The explicit
workspace session delegates through a narrow Executive recovery service to the
existing ExecutionManager and returns the canonical completed Objective.
Kernel and CLI remain unchanged.

Consequences:

- preserves the established application/workspace ownership boundary;
- prevents goal guessing and cross-workspace recovery;
- avoids leaking QueueItems or re-running the Executive pipeline;
- enables programmatic recovery while deferring operator-facing policy;
- requires a small composition pass-through in ExecutiveManager and factory.

### Option B — Kernel Recovery Boundary

Add a Kernel recovery method and route OperationalSession through it.

Consequences:

- gives execution and recovery a superficially symmetric Kernel surface;
- broadens Kernel beyond canonical Objective execution into persisted-ID lookup;
- requires every Kernel composition to supply a coherent recovery service;
- weakens the clearer rule that OperationalSession owns explicit workspace data.

### Option C — Immediate CLI Recovery Command

Add a workspace-plus-Objective-ID recovery command now.

Consequences:

- provides immediate operator access;
- selects CLI syntax, output, and operational error policy before the narrower
  application contract is proven;
- expands testing and public compatibility surface unnecessarily;
- risks conflating manual invocation with future retry/audit policy.

## Recommendation

Select **Option A**. It exposes only the smallest useful programmatic boundary
at the layer that already owns the explicit workspace, while preserving the
Kernel, CLI, and verified internal recovery contracts.

## Required Separate Work

- owner decision recording;
- bounded Option A implementation and verification, if selected;
- any later CLI/UI adapter, recovery audit evidence, or retry policy as its own
  decision and work order.
