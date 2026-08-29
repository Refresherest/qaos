# WO-084 — Objective Identity Propagation Assessment

## Objective

Define alternatives for propagating canonical Objective identity into Plan and
QueueItem without implementing migration or recovery.

## Architectural Context

OWNER-DECISION-012 makes Objective identity the canonical execution-attempt
identity and makes Plan and QueueItem non-owning references. WO-083 implements
the Objective identity foundation. Current Plan and QueueItem records retain
goal strings only.

## In Scope

- inspect Plan, PlanRegistry, PlannerManager, QueueItem, and QueueManager;
- inspect Council and ExecutionEngine construction and lookup paths;
- define identified and legacy reference behavior;
- define repeated equal-goal compatibility and persistence behavior;
- compare coherent propagation options and request an owner decision.

## Non-Goals

- product code, tests, entities, registries, or schemas;
- active-data migration or identity inference;
- recovery, retry, continuation, queue filtering, or guards;
- changes to Objective identity ownership;
- providers, models, credentials, OpenHands profiles, or deployment.

## Verification Requirements

- preserve goal-based compatibility while distinguishing equal-goal attempts;
- keep ObjectiveManager as identity source of truth;
- permit multiple QueueItems to reference one Objective ID;
- prohibit inferred identity for legacy Plan and QueueItem records;
- validate JSON, whitespace, secrets, scope, and runtime-data preservation.

## Stop Condition

Stop after proposal, decision request, verification, and handoff are recorded
and pushed. Do not select or implement the contract.
