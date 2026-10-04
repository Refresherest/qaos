# WO-177 — Durable Pilot Attempt-Authority Assessment

2026-10-04; baseline `fa25d5b` on `feat/operational-builder-chain`.
Authority: the owner's "next" after verified, local-only WO-176. Status:
COMPLETE — DESIGN PROPOSAL ONLY; independently ACCEPTED in VERIFICATION-128;
DECISION-REQUEST-024 remains open.

## Objective and scope

Assess how one `python-single` request can be claimed durably before transport
without creating a second queue authority or silently allowing a retry after an
uncertain SSH outcome. Reconcile the proposed contract with the existing
QueueItem, QueueManager, storage, generic recovery, WO-174 pilot controller and
WO-176 local bridge. Offer an owner choice before implementation.

In scope: read-only repository and primary SQLite documentation inspection,
architecture alternatives, verification and handoff records. Non-goals: product
or worker code, QueueItem or active-data mutation, migration execution, live
worker/cloud contact, credentials, transfer, Docker, generated-code execution,
new candidate/model call, dispatch, retry, publication or spending.

## Verified architecture boundary

- OWNER-DECISION-014 makes `objective_id` a shared reference, explicitly **not**
  QueueItem identity; OWNER-DECISION-016 makes `task_id` a Task correlation
  reference, not QueueItem identity. The current QueueItem has no own stable ID,
  and QueueRegistry permits multiple records with the same references.
- QueueManager loads the queue into memory once and rewrites its complete
  snapshot on `add`, `process`, `recover`, `clear` and `save`. JSONStore replaces
  a shared temporary file but has no interprocess lock, version comparison or
  durable flush. A claim-only lock would leave stale managers able to erase a
  claim or execute their stale pending object. Every queue writer and
  dispatch-eligibility reader must join one coordinated persistence boundary.
- Ordinary `process()` persists in `finally`, after worker execution. Explicit
  recovery (OWNER-DECISION-015) may reset and retry a failed QueueItem. Neither
  boundary is safe for a claimed or `UNKNOWN` one-attempt pilot without an
  explicit exclusion. OWNER-DECISION-011 requires recovery to be distinct from
  ordinary processing; this proposal does not repeal its generic recovery.
- WO-174 admission and response checks bind the originating in-memory
  QueueItem/Task object and require `pending` with no result. Every pilot
  request build currently generates a new UUID and nonce. A restart therefore
  needs stable reloaded identity and a frozen request envelope, not a rebuilt
  request. The broker replay marker is keyed by request ID and records hashes,
  not an outcome; a fresh ID can bypass it after SSH loss.
- WO-176's default-off deployment bridge is local and reviewed. It supplies no
  attempt claim, real dispatcher, authenticated status lookup or live evidence.

## Proposed CSA contract, subject to owner acceptance

1. QueueManager owns a new opaque, immutable QueueItem ID for newly created
   queue records. This identifies the persisted item, not a second execution
   attempt aggregate: `objective_id` remains the canonical Objective attempt
   reference and `task_id` the Task reference. Legacy rows without an
   ID remain readable and non-pilot-eligible; no ID is guessed from text,
   position or timestamp. Duplicate or ambiguous identity fails closed.
2. The canonical QueueItem record, not a sidecar job registry or broker marker,
   owns one immutable pilot-attempt envelope: item/objective/task IDs, exact
   candidate and acceptance Artifact IDs/digests, frozen request ID/nonce and
   request digest, runtime pins and claim time. It stores no candidate bytes or
   credentials. QueueItem.status owns the attempt lifecycle; do not create a
   second mutable state source in the envelope. `QueueItem.result` remains
   reserved for a validated, bounded response projection under
   OWNER-DECISION-036.
3. One interprocess transaction must verify a fresh pending item, absence of
   any prior pilot claim, exact canonical references and a current version;
   then persist the claim and `pilot_claimed` state before any network byte is
   sent. The same transaction refuses pre-existing ambiguous QueueItems with
   the pilot's `(objective_id, task_id)` and prevents a later `add` or
   ExecutionEngine requeue from creating an alias while the claim exists. All
   queue mutations and dispatch readers must reject stale snapshots. If
   commit/durability is uncertain, do not send.
   Because Artifact persistence is separate from Queue persistence, the
   controller must re-read the canonical Artifact IDs, bytes, digests and
   provenance against the frozen envelope immediately before send. Missing or
   drifted Artifacts stop without sending; the committed claim stays consumed
   and held, not rebuilt with a new request.
4. The first outbound write is the irreversible uncertainty boundary. Process
   loss after a committed claim but before any proven send may yield zero
   execution; loss during/after send, timeout or an invalid/missing response is
   `pilot_unknown`, not a failed attempt that can be retried. A hard crash may
   leave only durable `pilot_claimed`; that state is also held and
   non-dispatchable on restart even if transport may never have begun. Restart and
   competing dispatchers must not mint another request or resend the old one.
   No claim of exactly-once completion is possible from these signals.
5. A response received over the authenticated transport and exactly correlated
   to the frozen envelope may be validated and persisted once as
   `QueueItem.result`, with QueueItem.status `pilot_evidence_recorded`.
   An offline late response is not authenticated merely by its unkeyed SHA-256
   and matching fields; accepting one later requires a separately approved
   authenticated status channel or worker-signed durable receipt. The present
   broker has no outcome-query API, so `pilot_unknown` can remain held
   indefinitely for operator reconciliation. Generic `process()` and
   OWNER-DECISION-015 recovery must refuse *all* pilot-attempt QueueItems and
   recovery of their Objective; they must never reset an attempted pilot.
   Ordinary `process()` must also hold already-pending sibling QueueItems for
   that same Objective until separate adjudication, including after
   `pilot_evidence_recorded`, without blocking unrelated Objective IDs.
   Task and Objective lifecycle remain unchanged by merely recording pilot
   evidence. `cleanup_failed` and any result requiring operator review also
   remain quarantined. Their eventual adjudication is a separate architecture
   decision, not a PE inference from zero exit or candidate outcome.

## Persistence choice and proof obligations

DECISION-REQUEST-024 separates the queue-domain contract from its storage
choice. Recommended storage is one canonical SQLite queue store on a verified
local filesystem, with explicit transaction, uniqueness and durability settings
and a separately verified, non-destructive transition from the existing JSON
queue. SQLite alone is insufficient: all QueueManager selection, `add`,
`process`, `recover`, `clear`, `save` and public `Stores.queue_db.save(...)`
writes must use the new transactional boundary or explicitly fail closed on
claimed rows. A drop-in SQLite `load()/save()` that blindly replaces the full
snapshot would recreate the bug. Existing processes with old code or stale managers
must be fenced at any later cutover. The next implementation can use a fresh
local test workspace and fixture migration; no active JSON migration or
JSON/SQLite dual-authority period is permitted by this proposal. A complete
retrofit of the existing JSON store is an alternative,
but it must prove the same all-writer transaction, stale-version, crash and
platform guarantees. A new claim-only lock or sidecar marker is insufficient.

SQLite's own documentation explains its crash-atomic transaction mechanism and
that WAL with `synchronous=FULL` has stronger power-loss durability than WAL
with `NORMAL`; WAL also cannot be used over a network filesystem. These are
design inputs, not proof of this workspace's filesystem or an approved backend:

- <https://www.sqlite.org/atomiccommit.html>
- <https://sqlite.org/pragma.html#pragma_synchronous>
- <https://www.sqlite.org/wal.html>

## Later implementation acceptance gates

Test two independent processes claiming the same item, stale manager saves,
generic process/recovery races, same-Objective pending siblings and later
alias creation, separate Artifact
drift after claim, duplicate/missing
legacy IDs, a crash before claim commit, after commit but before send, during
send, after response but before result commit, and restart with a late
genuine/forged response. Offline late-response admission must fail absent the
separately approved authenticated channel or signed receipt. Use kill/fault
injection and verify the selected
filesystem and SQLite journal/sync configuration; do not describe unit tests
as proof against actual power loss. Verify that
one committed claim permits at most one outbound attempt, that any uncertain
state remains non-dispatchable and response-free, and that unrelated QueueItems
and existing generic recovery keep their approved behavior. Independently
review the implementation and migration plan before any active-data use.

## Verification and stop

Baseline: commit `fa25d5b02293a8c9b7a7c41353bf796ecfc8e8bf`, branch
`feat/operational-builder-chain`, Python 3.14.3, `architecture_inspect` 1.0.0
at 2026-10-04T17:21:02Z. Three pre-existing modified role-skill files and
unrelated untracked drafts/test directories were present and left untouched.
Read-only architecture inspection examined 201 Python source files and reported
its pre-existing static findings; none authorizes unrelated repair. Focused
current-contract tests passed: **89 passed**. No full runtime suite was rerun
because this work order changes only control-plane records.

STOP after the proposal, decision request and independent review. Owner
selection may authorize only a separately scoped local implementation and
tests. It does not approve active-data migration, a live dispatcher, worker
installation, one request or spending; those remain separate gates.
