# OWNER-DECISION-012 — Objective Attempt Identity

## Decision

The owner selected **Option A — Objective Identity Is Attempt Identity** from
DECISION-REQUEST-012.

## Architectural Contract

1. Objective owns the canonical immutable opaque identity for one operational
   invocation.
2. ObjectiveManager is the source-of-truth manager for that identity.
3. Plan and QueueItem may reference `objective_id`; they do not generate or own
   it.
4. Goal text remains compatibility and display data, not canonical identity.
5. Repeated equal goal text may represent distinct Objectives and invocations.
6. Legacy records without identity remain unassigned; QAOS must not infer
   identity from goal text, timestamps, ordering, or Task descriptions.
7. Identity enables future recovery selection but does not authorize recovery.

## Required Contracts Before Implementation

- opaque ID generation and injection;
- ObjectiveRegistry canonical and goal-compatibility behavior;
- ObjectiveManager load/save compatibility;
- PlanRegistry handling of repeated goal text;
- Plan and QueueItem reference propagation;
- legacy write-forward or migration policy;
- re-execution and recovery APIs.

## Exclusions

This decision does not authorize code, entity, registry, schema, migration,
propagation, recovery, retry, continuation guard, provider/model fallback, or
deployment changes.
