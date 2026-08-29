# FINDING-036 — Later-Call Implicit Continuation

## Status

`OPEN — IDENTITY PROPAGATED; EXPLICIT RECOVERY REQUIRED`

## Evidence

OWNER-DECISION-010 governs one failed QueueManager processing call only. The
public `process()` method selects every pending QueueItem and has no attempt,
batch, or failed-Objective guard.

An isolated WO-077 probe first produced the designated fail-fast state:

- calls: first item, second item;
- QueueItems: `completed, failed, pending`;
- second item raised `second task failure`.

Calling the same QueueManager's ordinary `process()` method again then:

- skipped the failed second item;
- executed the previously unattempted third item;
- persisted QueueItems and Tasks as `completed, failed, completed`.

## Impact

An ordinary queue-processing call can become a recovery/continuation mechanism
without an explicit recovery decision. QueueItem carries an objective goal
string but no attempt or batch identity, so the queue cannot robustly
distinguish a failed plan's remainder from unrelated pending work.

## Existing Boundary

WO-076 authorizes fail-fast semantics within one call and explicitly excludes
later-call behavior. ExecutionEngine is the only product caller, but
QueueManager.process remains publicly callable and drains all pending work.

## Scope Boundary

WO-077 is characterization only. Resolve later-call continuation through
DECISION-REQUEST-011 before changing QueueManager, QueueItem identity,
ExecutionEngine, or recovery behavior.

## Direction

OWNER-DECISION-011 selected an explicit recovery boundary with attempt
identity. Ordinary `process()` is not designated as recovery. Enforcement must
wait for a separately approved design because current Objective, Plan, and
QueueItem persistence has no canonical attempt identity.

OWNER-DECISION-012 now designates Objective identity as that canonical attempt
identity. FINDING-036 remains open until generation, registry, compatibility,
persistence, propagation, and recovery contracts are separately approved and
implemented.

OWNER-DECISION-013 selects the Objective identity generation, registry, and
legacy-loading contract. FINDING-036 remains open because the identity
foundation, downstream references, and explicit recovery operation have not
yet been implemented.

WO-083 implements and verifies the Objective identity foundation without
changing Plan, QueueItem, or queue-processing behavior. FINDING-036 remains
open pending separately governed downstream identity propagation and an
explicit recovery operation.

OWNER-DECISION-014 selects additive Plan and QueueItem Objective-ID references
with dual Plan indexes and legacy pass-through. FINDING-036 remains open until
the propagation contract and a separately governed recovery operation are
implemented and verified.

WO-086 implements and verifies the selected propagation contract without
changing QueueManager processing. FINDING-036 remains open because QAOS still
requires an explicit recovery selection and re-execution contract plus bounded
enforcement that prevents ordinary processing from acting as recovery.

WO-087 assesses that boundary. PROPOSAL-008 recommends targeted retry from the
single failed item through the identified attempt's pending remainder, plus an
ordinary-processing guard scoped by Objective ID. FINDING-036 remains open
pending OWNER-DECISION-015 and separately bounded implementation.

OWNER-DECISION-015 selects that contract. FINDING-036 remains open until the
explicit recovery operation and attempt-scoped ordinary-processing guard are
implemented and verified.

WO-089 identifies FINDING-037 as a direct implementation blocker: persisted
Plan Tasks and QueueItem actions have no canonical shared identity after reload.
FINDING-036 remains open while Task correlation is resolved through a separate
owner decision.
