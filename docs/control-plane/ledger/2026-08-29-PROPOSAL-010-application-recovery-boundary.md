# PROPOSAL-010 — Application Recovery Boundary

## Evidence Summary

- OperationalSession is the existing application-facing owner of one explicit
  Stores workspace and its ObjectiveManager.
- ExecutionManager owns the verified recovery operation and Objective lifecycle.
- create_executive constructs that ExecutionManager but currently retains it
  only inside ExecutivePipeline.
- Kernel exposes canonical Objective execution, but does not own the workspace
  ObjectiveManager or an explicit recovery service.
- The one-shot CLI creates an OperationalSession and currently accepts a new
  goal, not an existing Objective ID.
- Internal recovery returns QueueItems, which are execution details and should
  not become the application result contract.

## Recommended Contract

### Boundary

- Add `OperationalSession.recover_objective(objective_id)` as the only new
  application-facing recovery boundary.
- Require a non-empty canonical Objective ID. Never accept or infer a goal
  string as identity.
- The session's explicit workspace remains the complete lookup and mutation
  boundary; cross-workspace discovery is not introduced.

### Delegation

- create_executive retains its one explicitly constructed ExecutionManager as
  both the pipeline execution service and ExecutiveManager's narrow recovery
  service.
- ExecutiveManager delegates recovery directly to that service. Recovery must
  not traverse ExecutiveOrchestrator or ExecutivePipeline, because it must not
  re-run classification, Council delegation, planning, reflection, or learning.
- OperationalSession retains the composed ExecutiveManager and delegates the
  canonical ID to its recovery operation.
- Kernel remains unchanged; its existing method continues to govern new
  Objective execution only.

### Result and Failure

- On success, OperationalSession returns the canonical completed Objective from
  its workspace ObjectiveManager, not QueueItems or an ExecutionReport.
- Invalid, unknown, nonfailed, legacy, or inconsistent attempts fail through
  the existing internal preflight before execution-state mutation.
- Worker and persistence failures preserve the internal recovery exception and
  leave the Objective failed under the verified WO-092 contract.

### Explicit Exclusions

- No CLI command, Kernel method, UI action, automatic retry, retry budget,
  scheduling, migration, legacy association, or durable recovery audit record.
- No provider/model behavior and no new domain entity or recovery aggregate.

## Implementation Shape

If selected, a separate work order should change only ExecutiveManager,
create_executive, OperationalSession, their focused tests, and control-plane
records. Exact private attribute names and error wording remain implementation
details.
