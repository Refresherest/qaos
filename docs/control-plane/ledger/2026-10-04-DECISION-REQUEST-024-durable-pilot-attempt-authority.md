# DECISION-REQUEST-024 — Durable One-Attempt Pilot Authority

Status: OPEN — owner selection required. Basis: WO-177 after local-only
WO-176. No option here authorizes live dispatch or worker mutation.

## Decision 1 — Canonical QueueItem identity and claim

- **A (recommended):** assign a new opaque immutable `queue_item_id` when new
  QueueItems are admitted; embed one immutable pilot-attempt envelope in the
  canonical QueueItem record. The new ID identifies the queue record, not a
  second Objective attempt. Preserve Objective/Task IDs as references,
  `QueueItem.result` for validated response only, and legacy missing IDs as
  non-pilot-eligible without automatic backfill. Refuse an ambiguous existing
  `(objective_id, task_id)` pilot origin or a later alias while its claim exists.
- **B:** use `(objective_id, task_id)`, list position or broker request ID as
  QueueItem identity, or put the claim in a separate job registry. Reject:
  existing owner decisions make those references non-unique/non-authoritative,
  and the broker marker has no QueueItem outcome.

## Decision 2 — One transactional queue authority

- **A (recommended):** introduce a canonical, transactional SQLite queue
  store on a verified local filesystem, with cross-process claim/uniqueness,
  stale-write rejection and explicit durable commit before dispatch. Design
  and test a non-destructive JSON transition in a fresh local workspace; keep
  the old JSON read-only after any separately approved cutover, never as a
  concurrent source of truth. Every queue writer/selection path, including
  public `Stores.queue_db.save(...)`, must transact or refuse claimed rows;
  old-code processes and stale managers must be fenced at cutover. SQLite
  alone does not fix their stale-write behavior. Do not migrate active data
  under this decision alone.
- **B:** retain JSON but replace the queue persistence path with an
  all-writer/all-dispatch-reader interprocess transaction and version-CAS,
  including crash-durable file/directory sync on every supported platform.
  This avoids a store migration but has a larger custom concurrency/durability
  proof burden. A lock on the new claim path alone is not sufficient.

## Decision 3 — Uncertain transport and recovery

- **A (recommended):** commit the frozen request/Artifact claim and a
  `pilot_claimed` QueueItem state before any outbound byte. An ambiguous send,
  process/SSH loss, timeout or invalid response becomes `pilot_unknown` across
  restart when the transition can be persisted; a hard crash can leave
  `pilot_claimed`, which is equally held and cannot be resent. Never auto-retry,
  create a fresh request or use ordinary failed-item recovery for a claimed
  pilot or its Objective. A response over the original
  authenticated transport may be correlated and recorded once in
  `QueueItem.result` with status `pilot_evidence_recorded`. A later offline
  response needs a separately approved authenticated status channel or signed
  worker receipt; its unkeyed hash and matching fields do not suffice.
  Task/Objective lifecycle remains unchanged by evidence recording and needs
  a later adjudication decision. Immediately before send, re-read canonical
  Artifact IDs/bytes/digests/provenance. Drift stops sending but consumes the
  claim and requires explicit operator reconciliation. Preserve
  `QueueItem.result` as response evidence only.
- **B:** leave the item pending or mark it failed and reuse ordinary
  `process()`/recovery after loss. Reject: the first request may already have
  executed, while the restarted client can mint a new request ID.

## Decision 4 — Pilot lifecycle versus generic recovery

- **A (recommended):** use explicit non-pending QueueItem states
  `pilot_claimed`, `pilot_unknown` and `pilot_evidence_recorded`. A validated
  response changes only the pilot QueueItem and its bounded result; it does not
  automatically complete/fail the canonical Task or Objective. Generic
  `process()` must hold pending siblings until separate adjudication, including
  after `pilot_evidence_recorded`, while allowing unrelated Objectives. Generic
  recovery must refuse the whole Objective whenever it contains an attempted
  pilot item.
  A cleanup failure stays quarantined for operator review. Adjudicating the
  Task/Objective and any model-governance transition requires later authority.
- **B:** map pilot responses directly to ordinary QueueItem/Task/Objective
  completed or failed states. Reject for the first pilot: it requires
  cross-store atomic lifecycle changes and could expose a failed pilot to the
  existing retry operation.

## Requested response and release boundary

Approve, revise or reject 1A, 2A, 3A and 4A. If 2B is preferred, specify the
controller platforms/filesystems that the JSON transaction must support.
Approval permits a separate local-only implementation work order with explicit
schema/transition, state machine, queue-writer migration, crash/concurrency
tests and independent review. It does **not** permit active-data migration,
credential access, worker installation, candidate transfer, real dispatch,
Docker execution, model designation or spending. A later live gate still needs
fresh account/worker/network evidence, exact candidate and acceptance IDs,
cost ceiling, rollback owner and separate owner approval.
