# WO-086 — Objective Identity Propagation

## Objective

Implement the bounded Plan and QueueItem Objective-ID propagation contract
governed by OWNER-DECISION-014.

## Architectural Context

Objective owns canonical execution-attempt identity. Plan and QueueItem are
non-owning downstream references that retain goal text for compatibility.

## In Scope

- optional Objective-ID references on Plan and QueueItem;
- dual PlanRegistry indexes and complete-record iteration;
- conditional Plan and QueueItem load/save behavior;
- Objective-object Plan lookup in ExecutionEngine;
- identity propagation from CouncilManager and ExecutionEngine;
- focused and regression verification.

## Non-Goals

- active-data migration or inferred legacy association;
- recovery, re-execution, filtering, continuation, queue guards, or policy;
- Objective identity ownership changes;
- providers, models, credentials, OpenHands profiles, or deployment;
- unrelated architecture findings.

## Implementation Requirements

- preserve goal-string compatibility and raw-string construction;
- preserve equal-goal Plans as complete records;
- fail closed on duplicate non-null Plan Objective references;
- permit multiple QueueItems to share one Objective reference;
- omit missing references when re-saving legacy records.

## Verification Requirements

- focused propagation, planning, queue, and operational tests;
- full regression suite;
- compile, import, and architecture inspection;
- JSON, whitespace, secret, scope, and runtime-data preservation checks.

## Stop Condition

Stop after implementation, independent review, recording, commit, and push. Do
not continue into migration or recovery.
