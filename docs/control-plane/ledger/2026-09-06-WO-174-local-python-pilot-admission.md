# WO-174 — Local Python Pilot Admission Contract

2026-09-06; baseline `b22a353`; `feat/operational-builder-chain`.
Authority: OWNER-DECISION-036. Status: COMPLETE — LOCAL-ONLY.

## Objective

Implement and independently verify the local-only contract for one single-file,
dependency-free Python candidate Artifact and one independently authored acceptance
Artifact. Add a fixed launcher fixture and a bounded provider-neutral QueueItem
result projection without live installation, transfer or execution.

## In scope

- Add a composable worker-domain admission contract that derives exact candidate
  and acceptance member manifests from identified immutable Artifacts and existing
  Objective/Task correlations.
- Require exact roles and paths `candidate/candidate.py` and
  `acceptance/acceptance.py`; reject missing identities, digest mismatch, oversized
  UTF-8 content, self-acceptance and uncorrelated provenance.
- For this pilot only, cap each non-empty file at 64 KiB. Require Artifact
  provenance keys `objective_id`, `task_id` and `pilot_role` with exact canonical
  correlations, plus distinct non-empty creators. This is structural evidence of
  separate authorship, not identity attestation.
- Preserve the deployed synthetic launcher's bytes and digest. Implement the pilot
  as a separate, pinned root-owned launcher path under a distinct fixed policy.
- Add a fixed `python-single` launcher fixture whose command is owned by trusted
  infrastructure. Candidate bytes cannot select commands, image, network, mounts,
  environment, dependencies or test entrypoint.
- Extend the local broker/controller contract for the fixed pilot policy while
  preserving the synthetic `harmless` path.
- Validate the response before producing a bounded projection for the originating
  QueueItem.result. Do not automatically retry, publish, promote or change model
  governance.
- Add focused tests, full regression, compile and architecture inspection; obtain
  independent review.

## Non-goals

- No live key, worker, launcher, broker, sudoers, network, OCI or OmniRoute change.
- No model call, generated candidate creation, transfer or execution.
- No QAOS source, repository, patch, dependency, archive or credential handling.
- No new registry, job authority, queue lifecycle redesign, automatic result save,
  promotion, deployment, validation or designation.

## Verification and stop condition

Prove exact Artifact/Objective/Task correlation, canonical manifests, strict
single-file bounds, independent acceptance ownership, fixed launcher construction,
response rejection and bounded result projection. Run focused and full suites,
compile/static checks and independent review. Then STOP for a separate live pilot
authorization; do not install or execute the new fixture.

## Implemented local contract

- `src/qaos/workers/pilot_admission.py` derives a fixed two-member package from
  canonical Artifact IDs, byte digests and provenance; it retains the exact
  originating QueueItem object for result correlation without persisting it.
- `tools/qaos-worker/qaos_worker_pilot.py` builds one fresh bounded request and
  validates a supplied response into a <=4 KiB QueueItem.result projection. It
  opens no transport and does not save or mutate the QueueItem.
- The existing broker admits the pilot only when its separate policy, launcher
  path, launcher digest, image digest and fixture digest are explicitly pinned.
  The installed pilot path is fixed at
  `/usr/local/sbin/qaos-worker-pilot-launcher`; its root ownership, safe path
  metadata and digest are checked before use. The synthetic default is unchanged.
- The new launcher has fixed candidate/acceptance mounts and command, with
  `--pull=never`, no container network, bounded CPU/memory/process/output/time,
  no privilege elevation, exact cleanup checks and no candidate-selected flags.
  `.gitattributes` fixes this launcher's source bytes to LF line endings.
- Limit outcomes mark retained output as truncated. Missing or inconsistent
  post-launcher cleanup evidence is a `cleanup_failed` result requiring operator
  review; Docker runtime errors are not labeled candidate failures.

See `2026-10-04-VERIFICATION-125-wo-174.md` for focused/full test results and
independent review. A passing acceptance exit is not proof of candidate quality,
model validation or designation. Live installation, transfer and execution remain
unauthorized and untested.
