# FINDING-037 — Task and Queue Action Identity Gap

## Status

`RESOLVED — WO-091`

## Evidence

Plan persistence embeds Task records in `plans.json`. Queue persistence embeds a
second serialized copy of the same Task as QueueItem `action`. Neither copy has
canonical Task identity.

A bounded WO-089 reload probe created one identified Objective, one failed Plan
Task, and one failed QueueItem referring to that Task. Reloading PlannerManager
and QueueManager produced:

- `SAME_OBJECT False`
- Plan Task status: `failed`
- Queue action status: `failed`
- after resetting only the queue action: Plan Task `failed`, queue action
  `pending`

The probe used workspace-local temporary data and removed it afterward. Active
runtime data was unchanged.

## Impact

OWNER-DECISION-015 requires durable recovery to reset the failed QueueItem and
its failed Task, then save coherent Plan state. After process restart, QAOS
cannot determine which Plan Task is the queue action without inferring from
description, list position, or timestamps. Updating only the queue copy creates
split-brain execution state.

## Architectural Boundary

Objective identity selects the attempt but does not identify one Task within
that attempt. QueueItem identity is not authorized, and its Objective reference
is intentionally non-unique. Recovery must not infer Task correlation.

## Required Decision

Select a canonical Task identity owner and QueueItem action-reference contract
through DECISION-REQUEST-016 before implementing durable recovery.

OWNER-DECISION-016 selects PlannerManager-assigned opaque Task IDs with
non-owning QueueItem action references. FINDING-037 remains open until that
foundation is implemented and verified across persistence reload.

WO-091 implements and verifies Task identity assignment, Plan lookup, QueueItem
action references, duplicate/mismatch rejection, legacy pass-through, and the
operational pre-queue assignment path. Durable Task correlation now survives
independent Plan and Queue reload, resolving FINDING-037.
