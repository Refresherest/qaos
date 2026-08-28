# WO-052 — Queue Worker Composition

## Objective

Allow an explicitly composed QueueManager to process items through a
caller-selected worker service without crossing into module state.

## Architectural Context

QueueManager already owns isolated Stores and registry state, and
ExecutionEngine already accepts an explicit QueueManager. Worker resolution was
the remaining implicit boundary in queue processing.

## Requirements

1. QueueManager accepts an explicit worker service.
2. `process()` resolves the established `default` worker from that service.
3. Selected-worker item changes persist through the QueueManager's Stores.
4. The default constructor retains the existing module worker_manager.

## Scope

- QueueManager worker-service injection
- Explicit processing and default compatibility tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- No worker registry, agent, selection policy, queue ordering, or schema change.
- No provider, model, credential, Content OS, or other stage change.

## Verification Requirements

- Prove the selected worker executes and its result persists in selected Stores.
- Prove default worker-service compatibility.
- Run focused and full regression checks, import sweep, compilation,
  architecture inspection, and active-data comparison.

## Stop Condition

Stop after FINDING-025 is independently reviewed and WO-052 is published.
