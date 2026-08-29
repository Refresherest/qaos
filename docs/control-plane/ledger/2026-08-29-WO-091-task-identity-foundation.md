# WO-091 — Task Identity Foundation

## Objective

Implement the bounded Task identity and QueueItem action-reference foundation
governed by OWNER-DECISION-016.

## Architectural Context

Plan is the canonical Task owner. Durable recovery requires QueueItem actions to
correlate with Plan Tasks after independent persistence reload.

## In Scope

- optional immutable Task identity;
- PlannerManager-injected assignment before persistence or queueing;
- explicit Plan Task lookup and duplicate-ID rejection;
- conditional Plan Task serialization and legacy omission;
- QueueItem non-owning Task references and consistency validation;
- QueueManager conditional reference persistence;
- focused and regression verification.

## Non-Goals

- recovery, ordinary-processing guards, migration, or legacy association;
- QueueItem identity, automatic retry, retry policy, scheduling, or audit;
- Kernel, CLI, UI, provider, model, credential, or deployment changes;
- unrelated architecture findings.

## Implementation Requirements

- assign new Task IDs before persistence and queue construction;
- never assign identity to loaded legacy Tasks during unrelated saves;
- fail closed on duplicate or mismatched non-null Task references;
- preserve raw Task and QueueItem compatibility when identity is absent;
- keep PlannerManager as the only Task ID generator.

## Verification Requirements

- focused Task, Plan, Queue, and operational pipeline tests;
- full regression suite;
- compile, import, and architecture inspection;
- JSON, whitespace, secret, scope, and active-data preservation checks.

## Stop Condition

Stop after implementation, independent review, recording, commit, and push. Do
not continue into recovery implementation.
