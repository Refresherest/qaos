# DECISION-REQUEST-008 — Pre-Execution Failure Ownership

## Status

`OWNER DECISION REQUIRED`

## Evidence

OperationalSession creates and persists an Objective before invoking Kernel.
Classification, council delegation, and planning occur before ExecutionManager
starts that Objective. A failure in those stages therefore leaves it pending.

WO-059 already assigns `start -> complete/fail` lifecycle ownership to
ExecutionManager after execution begins. This decision concerns only an
exception that escapes while the Objective is still pending.

## Decision

Choose who owns the pre-execution failure transition.

### Option A — OperationalSession Owns Pending Failure (Recommended)

OperationalSession catches an exception from Kernel. If the Objective remains
`pending`, it marks that Objective failed through its shared ObjectiveManager,
then re-raises the original exception unchanged. If another component already
transitioned the Objective, the session does not overwrite that state.

Consequences:

- closes the exact application-created lifecycle gap;
- preserves ExecutionManager ownership after `start`;
- uses the same manager that created and persisted the Objective;
- keeps Kernel and Executive provider-neutral and lifecycle-agnostic;
- requires explicit tests for conditional failure, persistence, and unchanged
  exception propagation.

### Option B — Executive Boundary Owns Pre-Execution Failure

Inject ObjectiveManager into ExecutiveOrchestrator and let it mark a pending
Objective failed when its pipeline raises.

Consequences:

- covers Executive calls outside OperationalSession;
- adds persistence authority to an orchestrator that currently owns only
  ExecutionResult coordination;
- overlaps with ExecutionManager lifecycle authority and broadens Executive
  composition contracts.

### Option C — Preserve Pending State

Document pending as intentional for failures before execution starts.

Consequences:

- adds no code or ownership;
- preserves distinction between never-started and started work;
- leaves the CLI failure and persisted Objective state inconsistent for
  operators and requires separate recovery policy.

## Recommendation

Select **Option A**. OperationalSession created the Objective and already owns
the correct ObjectiveManager. A conditional `pending -> failed` transition
closes the reproduced gap without revising WO-059 or introducing persistence
into ExecutiveOrchestrator.

## Explicitly Deferred

- failures after ExecutionManager completes but reflection or learning fails;
- retry, resume, rollback, and recovery queues;
- persisted error details or schema changes;
- Content OS, provider/model routing, fallback execution, and deployment.
