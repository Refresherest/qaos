# WO-178 — Local Durable Pilot Attempt Authority

2026-10-04; baseline `777151a` on `feat/operational-builder-chain`.
Authority: owner approved DECISION-REQUEST-024 options 1A, 2A, 3A and 4A.
Status: ACCEPTED — LOCAL ONLY (VERIFICATION-129); no live gate.

## Objective and architectural context

Implement the approved one-attempt `python-single` pilot authority without a
second queue source of truth. A newly admitted QueueItem gains an opaque,
immutable queue record ID. One canonical QueueItem may durably own a frozen
pilot request and its non-retryable state. A fresh, explicitly selected local
SQLite queue store serializes all queue writes and dispatch selection; the
existing JSON store remains the default and active data is not migrated.
The frozen claim must commit before any outbound byte could be sent.

The source-of-truth hierarchy, Objective/Task correlation identities,
validated-response-only `QueueItem.result`, and
VERIFIED != VALIDATED != DESIGNATED remain unchanged. Legacy QueueItems
without an ID remain readable but not pilot-eligible.

## Files and domains in scope

- QueueItem identity, queue serialization and QueueManager's SQLite-specific
  transactional add, process, recovery, clear, save and pilot state paths.
- Explicit opt-in SQLite queue storage and fresh-fixture import, with the
  existing JSON default left compatible.
- Local pilot request claim and immediate pre-send canonical Artifact
  revalidation, without a sender or network connection.
- Narrow higher execution-path guard to prevent attempted-pilot Objectives
  from being marked complete or failed by generic execution/recovery.
- Focused and regression tests; control-plane decision, verification and
  handoff records.

## Implementation requirements

1. Assign a QueueItem ID only at new admission; never derive or backfill a
   legacy ID. Reject duplicate identity and ambiguous pilot-origin aliases.
2. Embed one immutable, bounded attempt envelope in the canonical QueueItem:
   exact request header and digest, Item/Objective/Task refs, candidate and
   acceptance Artifact refs, runtime pins and claim time; no payload bytes or
   credentials. Commit `pilot_claimed` atomically before any potential send.
3. SQLite queue operations use a fresh persisted snapshot inside one
   cross-process transaction. Public blind snapshot save refuses. Ordinary
   dispatch reserves its item before worker execution, and holds all pending
   siblings of an attempted-pilot Objective, including after evidence.
4. An uncertain attempt is held as `pilot_claimed` or `pilot_unknown`, never
   retried or assigned a fresh request. Generic recovery refuses the whole
   attempted-pilot Objective. Evidence recording, if exercised locally, must
   require an original authenticated transport binding; an offline frame is
   not admitted by matching IDs or an unkeyed digest. No pilot evidence may
   complete/fail Task or Objective automatically.
5. Re-read canonical Artifact IDs, bytes, digests and provenance immediately
   before any future sender uses the frozen request. Drift consumes the claim,
   marks it unknown when durable transition is possible, and prevents send.
6. No coexisting JSON/SQLite authority in one selected workspace. Fixture
   import is allowed only into an empty local test workspace and preserves
   legacy rows; active data remains untouched.

## Explicit non-goals

No active-data migration or cutover; no OCI/SSH/Docker or worker mutation; no
credentials, candidate transfer, generated-code execution, live dispatch,
retry, authenticated late-status service, adjudication of Task/Objective,
model designation, account spending or live gate. The local claim API is not
a live sender.

## Verification and stop condition

Verify syntax/imports, focused identity/claim/concurrency/crash/alias/stale
writer/Artifact-drift/recovery/sibling tests, existing regression suite and
architecture inspection. Record filesystem and SQLite settings and state that
fault injection is not proof of real power-loss durability. Obtain an
independent QAOS Reviewer result. Then record what did and did not change,
and **STOP**. Any active-data transition or live pilot requires a separate
work order and fresh owner approval.

## Implementation evidence (2026-10-07)

- Explicit `queue_backend="sqlite"` uses a local SQLite queue with WAL,
  `synchronous=FULL`, `BEGIN IMMEDIATE`, uniqueness and revision checks. It
  refuses blind saves and coexistence with `queue.json`. The JSON default and
  active queue remain unchanged. A one-time, empty-workspace fixture import
  preserves legacy rows without assigning IDs.
- New QueueItems receive immutable IDs. The canonical item owns one frozen
  request/Artifact envelope and `pilot_claimed`/`pilot_unknown` state. A
  process-only, non-persisted 32-byte capability is required to consume the
  claim into `pilot_unknown` before any framed bytes can be returned; restart
  cannot recreate that capability. No transport was added.
- Request admission and storage enforce an exact field allowlist and digest;
  admission additionally checks the reviewed protocol, UUID/nonce, two-minute
  window, fixed member paths and runtime pins. Admission and one-use release
  re-read canonical Artifact metadata and bytes from the queue's selected
  workspace, with no caller-supplied Artifact manager at release. An offline
  response cannot become `pilot_evidence_recorded`: no authenticated original
  transport writer exists in this local work order.
- Generic SQLite process reserves under a fresh transaction and compares the
  exact reserved row before result commit. Same-Objective pilot siblings and
  generic recovery are held; unrelated generic work/recovery remains
  available. Higher Objective/Plan executive execution against this new
  SQLite workspace is refused until a separate cross-store lifecycle gate.
- Focused final tests: **126 passed** across the new queue/store/pilot tests
  and existing pilot admission/controller tests. Full regression in a fresh
  system-temp directory: **748 passed, 1 skipped**. An earlier full run inside
  the repository had four intermittent Windows `JSONStore.os.replace`
  permission errors; all four affected cases passed on immediate isolated
  rerun, and the subsequent full system-temp run passed. Compile and diff
  checks passed. Architecture inspection examined 203 Python files and
  reported only the pre-existing static finding categories. Fault injection
  is not proof against actual power loss.
- The independent reviewer identified two material gaps during review:
  generic finalizers could overwrite a concurrent running-row edit, and the
  first request/release API accepted an under-validated or reconstructible
  claim. Exact-row compare, strict request/schema checks, and volatile
  one-use release capability were added with targeted regression tests. The
  final reviewer found a third material gap: a caller could supply a stale
  copy of the Artifact store at release. The release API no longer accepts
  that manager, and both admission and release read the queue-selected
  workspace. The reviewer then returned **ACCEPT** on the post-fix tree.

STOP at this accepted local checkpoint. Do not migrate active data, send a
pilot request, install a worker, adjudicate a Task/Objective or infer a model
governance change from these local tests.
