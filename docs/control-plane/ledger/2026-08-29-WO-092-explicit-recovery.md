# WO-092 — Explicit Attempt Recovery

## Objective

Implement the bounded internal recovery contract selected by
OWNER-DECISION-015 for an identified failed Objective attempt.

## Architectural Context

Plan owns canonical Task state, Queue owns execution state, and
ExecutionManager owns Objective lifecycle. Objective and Task identities now
provide durable correlation across independent reloads.

## In Scope

- fail-closed recovery preflight across Objective, Plan, and Queue;
- retry of exactly one failed QueueItem followed by later pending items;
- durable synchronization of Queue action and canonical Plan Task state;
- Objective lifecycle transitions owned by ExecutionManager;
- ordinary-processing guard for identified attempts with a failed item;
- focused and regression verification.

## Non-Goals

- automatic retry, retry budgets, scheduling, migration, or legacy association;
- Kernel, CLI, UI, or other public recovery exposure;
- provider, model, credential, deployment, or audit-evidence changes;
- unrelated architecture findings.

## Implementation Requirements

- select recovery only by canonical `objective_id`;
- require exactly one failed QueueItem and no earlier pending QueueItem;
- validate all selected QueueItems against canonical Plan Tasks before mutation;
- reset only the failed item and retry it before later pending items;
- preserve completed and unrelated items;
- persist coherent Plan, Queue, and Objective failure state if retry fails again;
- preserve the original execution exception.

## Verification Requirements

- focused durable reload, selection, lifecycle, synchronization, and guard tests;
- negative preflight and repeated-failure tests;
- full regression suite;
- compile, import, architecture, scope, secret, and active-data checks.

## Stop Condition

Stop after implementation, independent review, recording, commit, and push. Do
not expose recovery publicly or begin another work order.
