# WO-169 — Worker Validation Exchange Contract

2026-09-05; baseline `ebba9d9`; `feat/operational-builder-chain`.
Authority: the owner replied "proceed" after VERIFICATION-121 identified a
bounded immutable input manifest and authenticated result transport as the next
architecture work. Objective: inspect existing ownership/identity contracts and
produce an implementation-ready proposal plus owner decision request. Status:
COMPLETE / decision required before implementation.

## Scope and non-goals

- Reconcile candidate/input/result ownership with existing Artifact, Objective,
  Task and QueueItem contracts.
- Define strict request/response schemas, transport authentication, replay and
  size limits, refusal behavior, lifecycle, evidence and teardown boundaries.
- Compare transport and artifact-identity options and recommend one staged path.
- Do not change product code, schemas, worker users/keys/sudoers, SSH, launcher,
  Docker, gVisor, networking, active data or live cloud resources.
- Do not create credentials, expose a service, transfer candidate files, stage
  QAOS source or execute generated code.

## Existing contract evidence

- Objective and Task IDs are canonical opaque correlations. Plan owns Task
  identity; QueueItem copies `objective_id` and `task_id` as non-owning references.
- QueueItem.result is the existing execution-evidence location and is persisted by
  QueueManager. A worker exchange must not create a second job/status registry.
- ArtifactManager owns candidate bytes, but Artifact currently has only title,
  type, creator, objective and content. ArtifactRegistry is title-keyed and a
  second registration with the same title replaces the first entry.
- Existing executable intents accept only reviewed deterministic source/templates.
  They must not be widened to carry generated code or remote-worker parameters.
- WO-168's launcher is fixed-fixture infrastructure and exposes no candidate-input
  surface. Its verified controls are prerequisites, not a transport API.

The current Artifact contract therefore cannot truthfully identify an immutable
generated candidate by title alone. A transport manifest could hash a transient
snapshot, but QAOS would not yet have a durable canonical identity for those exact
bytes. Generated-candidate admission remains blocked until the owner resolves this
source-of-truth gap.

## Proposed ownership map

| Concern | Proposed owner |
| --- | --- |
| Objective and Task correlation | Existing canonical Objective/Task IDs |
| Candidate and independent acceptance bytes | Existing Artifact domain after explicit immutable identity/digest/provenance evolution |
| Validation request projection | Provider-neutral integration DTO derived from canonical IDs and Artifact digests; no registry |
| Transfer authentication and replay state | Restricted worker broker plus controller transport adapter |
| Runtime enforcement | Root-owned worker broker/launcher and pinned runtime policy |
| Validation outcome and bounded diagnostics | Existing QueueItem.result |
| Accepted artifact bytes and provenance | Existing ArtifactManager; never candidate self-promotion |
| Promotion/designation | Existing owner/reviewer governance outside worker |

No Oracle, Docker, gVisor, SSH or model identifier becomes a canonical QAOS
product identity. Infrastructure details are evidence fields and adapter policy.

## PROPOSAL-014 — Option A: restricted SSH framed exchange

Use the existing restricted TCP/22 management path without exposing another
listener. Create a dedicated transport OS identity and ED25519 key pair under a
separate implementation work order. The private key remains controller-side and
outside source control. Its worker `authorized_keys` entry uses OpenSSH `restrict`
plus one root-owned forced broker command; no PTY, agent forwarding, port forwarding,
user shell, SFTP or arbitrary requested command is allowed.

The forced unprivileged entry may invoke exactly one root-owned broker through one
exact sudoers rule. It must not receive general Docker, shell or filesystem sudo.
The broker itself owns validation, staging, the fixed runtime call, result framing
and exact cleanup. Candidate code never sees the SSH channel, key, broker socket,
Docker socket, host staging path or result collector.

### Wire framing

One controller-initiated SSH session carries one request and one response. Each
frame is `8-byte unsigned big-endian length || bytes`. The first request frame is
UTF-8 JSON capped at 64 KiB. Member byte frames follow in the manifest's canonical
path order. There is no tar/zip/archive parser, compression, symlink, device, mode,
owner, timestamp, extended attribute or caller-selected destination.

The response is one UTF-8 JSON frame capped at 2.25 MiB, followed by EOF. Any extra
byte, premature EOF, length overflow, invalid UTF-8/JSON, duplicate key, unknown
field, non-canonical encoding or trailing frame is a protocol error. The controller
does not deserialize executable objects or automatically import/publish files.

### Request v1 schema

Exact top-level fields:

```text
protocol             = "qaos.worker.validation"
version              = 1
request_id           = lowercase UUIDv4
nonce                = base64url 32 random bytes, no padding
created_at           = UTC RFC3339 second precision
expires_at           = UTC RFC3339, > created_at and <= created_at + 5 minutes
objective_id         = existing non-empty canonical ID
task_id              = existing non-empty canonical ID
candidate_artifact   = {artifact_id, content_sha256}
acceptance_artifact  = {artifact_id, content_sha256}
members              = ordered array of member records
runtime              = exact expected launcher SHA-256, image digest and policy ID
```

Each member record has exactly `role`, `path`, `size`, and `sha256`. Role is
`candidate` or `acceptance`. Paths are ASCII POSIX relative names, 1–128 bytes,
restricted to `[A-Za-z0-9._/-]`, without leading/trailing slash, empty, `.` or
`..` segments, backslash, control characters or case-insensitive duplicates.
Canonical ordering is `(role, path)` byte order. At most 32 regular members,
1 MiB/member and 8 MiB total are accepted. Each frame length and SHA-256 must match
before any runtime creation. The broker assigns fixed read-only locations/modes.

`runtime` must exactly match the installed approved values; the caller cannot
select an image, executable, entrypoint, environment, network, mount, device,
capability, UID, limit or Docker flag. The independent acceptance artifact is
separately owned and digested; candidate members cannot replace it.

### Authentication and replay

OpenSSH host-key pinning authenticates the worker to the controller. The dedicated
restricted client key authenticates the controller to the forced broker. The broker
atomically creates a root-owned request marker keyed by `request_id` and nonce
before staging; duplicates, expired/future requests and concurrent work fail closed.
The marker records only bounded hashes/state and survives until result collection
and cleanup are both confirmed. The controller also refuses repeated response IDs.

This authenticates the transport endpoints and binds one response to one request.
It does not make a compromised worker truthful or replace artifact/reviewer authority.
No key is reused from OmniRoute, the admin SSH identity, a model provider or OCI.

### Response v1 schema

Exact top-level fields:

```text
protocol/version/request_id/nonce/objective_id/task_id
candidate_artifact/acceptance_artifact
worker_instance_id
launcher_sha256/runtime_version/image_digest/policy_id
started_at/completed_at
outcome
exit_code/oom_killed/termination_reason
stdout/stderr = {bytes, sha256, truncated, text_preview}
resource_evidence
acceptance_results
cleanup
response_sha256
```

`outcome` is one of `completed`, `candidate_failed`, `policy_rejected`,
`limit_terminated`, `runtime_failed`, or `cleanup_failed`. Cleanup failure always
dominates success. Preview strings are UTF-8 replacement-decoded and bounded;
hash/length cover the original retained bytes. Acceptance results have exact
test IDs from the independent bundle, observed status/duration and bounded evidence.
Candidate-produced success text cannot set outcome or acceptance status.

The broker calculates `response_sha256` over canonical JSON with that field omitted.
The controller validates framing, all request correlations/digests, expected worker
host key, launcher/runtime/image/policy identities, timestamps, enums, bounds,
cleanup and response hash before persisting a provider-neutral projection in the
existing QueueItem.result. It never records private keys, environment, host paths,
raw unbounded output or provider credentials.

### Failure and lifecycle

Validation occurs in this order: SSH authentication; frame/schema/bounds; replay;
member hashes; immutable staging; policy/runtime identity; execution; trusted
acceptance; bounded collection; process/container/staging cleanup; response. Failure
before execution creates no container. Any post-creation error kills the exact
container/process tree and cleans exact owned staging. Unknown cleanup state returns
`cleanup_failed`, quarantines admission and requires operator inspection.

There is no automatic retry. A new attempt requires a new request ID/nonce and the
existing QAOS recovery/attempt decision; it never overwrites prior evidence. Loss of
SSH yields UNKNOWN to the controller until an authenticated status/cleanup check.

## Artifact identity prerequisite

### A1 — Additive immutable Artifact identity (recommended)

Before generated-candidate transfer, evolve Artifact with an injected opaque
`artifact_id`, canonical byte-oriented `content_sha256` and bounded provenance;
use dual ID/title lookup, reject duplicate IDs and preserve legacy missing-ID loads
without write-forward. Title remains a display/compatibility key, not immutable byte
identity. The exact content canonicalization for text/binary/multi-member artifacts
requires its own decision and tests.

Consequences: aligns bytes with existing Artifact authority and proven identity
patterns, supports exact correlation, but requires a separate core schema work order.

### A2 — Title plus transient manifest digest

Keep current Artifact unchanged and identify the transfer by title plus a computed
digest. Smaller change, but title replacement means the manifest may no longer map
to canonical retained bytes. Not recommended for generated-candidate admission.

### A3 — Store candidate bytes in QueueItem.result

Makes the execution record self-contained but duplicates/inverts Artifact authority,
inflates queue persistence and confuses evidence with artifact ownership. Reject.

## Transport alternatives

### B — Existing admin SSH plus manual SFTP/SCP

Fewer components, but reuses broad administrative authority, relies on archive/path
handling or mutable operator steps and cannot provide a narrow machine contract.
Acceptable only for fixed-fixture maintenance already performed, not generated jobs.

### C — HTTPS/mTLS worker service

Can support structured APIs and independent client/server certificates, but adds a
public listener, certificate lifecycle, service daemon and larger attack surface
before one-job semantics are proven. Defer; do not create a new ingress rule.

### D — Worker polling object storage/queue

Supports later scale but adds cloud services, credentials, cost, worker egress and
provider coupling. It also risks making cloud transport the source of truth. Defer.

## Recommendation and decision boundary

Select Option A with prerequisite A1. First implement and verify Artifact identity,
digest and provenance locally under a separate owner-approved work order. Then create
a separate restricted-transport setup work order for the dedicated OS/key identity,
forced broker, exact sudoers rule, framed parser and synthetic exchange tests. Do not
combine credential creation, product schema evolution and live worker mutation.

Approval of this proposal does not authorize any implementation, credential creation,
live worker change, candidate transfer or generated-code execution.

## Verification and stop condition

Evidence: read-only repository/source/control-plane inspection; no runtime or product
tests rerun for a design-only record. JSON and whitespace checks apply. Existing
dirty/untracked owner files, active data, worker, OmniRoute, credentials and OCI state
remain untouched.

WO-169 is complete. Stop for the owner decisions in DECISION-REQUEST-021.
