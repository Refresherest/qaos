# OWNER-DECISION-017 — Application Recovery Boundary

## Decision

The owner selected **Option A — OperationalSession Boundary** from
DECISION-REQUEST-017.

## Governing Contract

### Application Boundary

- OperationalSession will expose an explicit recovery operation selected only
  by canonical `objective_id`.
- The identifier must be a non-empty string. Goal strings are never accepted or
  inferred as Objective identity.
- The session's explicitly selected Stores workspace is the complete lookup and
  mutation boundary; cross-workspace discovery is prohibited.

### Composition and Delegation

- create_executive will retain one explicitly constructed ExecutionManager as
  both ExecutivePipeline's execution service and ExecutiveManager's narrow
  recovery service.
- ExecutiveManager will delegate recovery directly to ExecutionManager.
- Recovery must bypass ExecutiveOrchestrator and ExecutivePipeline and therefore
  must not re-run classification, Council delegation, planning, reflection, or
  learning.
- OperationalSession will retain the composed ExecutiveManager and delegate the
  canonical Objective ID through that recovery service.
- Kernel and CLI remain unchanged.

### Result and Failure

- Successful application recovery returns the canonical completed Objective
  from OperationalSession's ObjectiveManager.
- QueueItems and ExecutionReport remain internal and are not the application
  result contract.
- Existing WO-092 preflight, ordering, state synchronization, lifecycle, and
  original-exception behavior remain authoritative and unchanged.

## Scope Boundary

This decision authorizes a separate bounded implementation across
ExecutiveManager, create_executive, OperationalSession, focused tests, and
control-plane records only. It does not authorize Kernel, CLI, UI, automatic
retry, retry budgets, scheduling, migration, legacy association, durable audit
evidence, provider/model changes, or unrelated work.
