# WO-053 — Worker-to-Agent Composition

## Objective

Allow an explicitly composed queue-worker chain to retain caller-selected worker
and agent ownership without crossing into module registries.

## Architectural Context

WO-052 made QueueManager's worker service explicit. WorkerManager, DefaultWorker,
and AgentManager still selected module registries and services internally.

## Requirements

1. AgentRegistry and WorkerRegistry are instantiable; compatibility functions
   retain their default registries.
2. AgentManager accepts an explicit AgentRegistry.
3. DefaultWorker accepts an explicit AgentManager-compatible service.
4. WorkerManager accepts explicit registry and default worker services.
5. Default constructors preserve existing registrations and behavior.

## Scope

- Agent and worker registry lifecycles
- AgentManager, DefaultWorker, and WorkerManager dependency injection
- Explicit queue-to-agent, default compatibility, and isolation tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- No Agent skill resolver, worker policy, execution semantics, or queue schema change.
- No provider, model, credential, Content OS, or other executive-stage change.

## Verification Requirements

- Prove a selected Agent executes through selected WorkerManager and QueueManager.
- Prove worker and agent registry isolation.
- Prove default compatibility.
- Run focused and full regression checks, import sweep, compilation,
  architecture inspection, and active-data comparison.

## Stop Condition

Stop after FINDING-026 is independently reviewed and WO-053 is published.
