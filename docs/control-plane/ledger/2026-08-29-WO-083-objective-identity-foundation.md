# WO-083 — Objective Identity Foundation

## Objective

Implement the bounded Objective identity foundation governed by
OWNER-DECISION-013.

## Architectural Context

Objective identity is the canonical execution-attempt identity. The existing
Objective domain, ObjectiveManager construction boundary, and ObjectiveRegistry
remain authoritative; this work introduces no additional attempt aggregate.

## In Scope

- optional immutable `Objective.objective_id`;
- manager-injected opaque ID generation for new Objectives;
- distinct legacy loading without inferred identity;
- canonical ID and latest-by-goal registry indexes;
- explicit ID lookup and complete-record iteration;
- persistence of identity for new records while omitting it from legacy records;
- fail-closed duplicate non-null ID handling;
- focused and regression verification.

## Non-Goals

- Plan or QueueItem identity fields or propagation;
- active-data migration or inferred legacy identity;
- recovery, retry, continuation, or queue guards;
- provider, model, credential, OpenHands, Content OS, or deployment changes;
- unrelated architecture findings.

## Implementation Requirements

- preserve existing goal-string and Objective-object lookup compatibility;
- retain every equal-goal Objective in complete-record persistence;
- keep ID generation deterministic under injected test generators;
- never replace an already assigned Objective identity;
- reject duplicate non-null identities without corrupting registry state.

## Verification Requirements

- focused Objective identity tests;
- relevant Objective lifecycle and storage tests;
- full regression suite;
- compile and full package import sweep;
- architecture inspection, JSON, whitespace, secret, scope, and runtime-data
  preservation checks.

## Stop Condition

Stop after this bounded foundation is implemented, independently reviewed,
recorded, committed, and pushed. Do not continue into downstream propagation or
recovery.
