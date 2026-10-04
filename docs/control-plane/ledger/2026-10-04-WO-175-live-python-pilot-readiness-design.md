# WO-175 — Live Python Pilot Readiness Design

2026-10-04; baseline `83f252b`; branch `feat/operational-builder-chain`.
Authority: the owner's "Next" after WO-174. Status: COMPLETE — DESIGN ONLY;
DECISION-REQUEST-023 remains open. This work order does not authorize a live pilot.

## Objective

Define the smallest separately approvable path from WO-174's verified local
contract to one live `python-single` attempt on `qaos-worker`. Identify the
missing deployment, attempt, recovery, cost and security evidence before any
worker mutation, candidate transfer or generated-code execution.

## Architectural context and verified boundary

- OWNER-DECISION-036 authorized local implementation and review only. WO-174 and
  VERIFICATION-125 completed that scope; they did not install or run the pilot.
- Canonical candidate and independently authored acceptance bytes belong to
  distinct immutable Artifacts. Objective/Task IDs correlate the request;
  `QueueItem.result` is the existing execution-evidence destination. A distinct
  nonempty `creator` value is structural separation, not identity attestation.
- The broker's default `BrokerConfig()` admits only the installed synthetic
  route. The pilot requires explicitly pinned policy, launcher path/digest,
  image digest and fixture digest. No reviewed live enablement path exists.
- The old transport installation and rollback scripts affect the entire
  synthetic transport. They are not an incremental pilot upgrade/rollback.
- The pilot controller prepares and validates a request/response but neither
  opens SSH nor persists a result. The synthetic probe is not a real-pilot
  operation. The broker replay marker stores request hashes, not a durable
  outcome. SSH loss after dispatch therefore means `UNKNOWN`, not failure or
  permission to retry.
- The local admission check accepts a pending QueueItem with `result is None`;
  each request build generates a new ID/nonce. `QueueManager.process()` can
  execute pending items, while its whole-registry JSON save has no atomic
  per-item claim or interprocess compare-and-set. OWNER-DECISION-036 assigns
  `QueueItem.result` to the validated response projection, not a pre-dispatch
  reservation. A durable one-attempt/UNKNOWN recovery contract is therefore
  **unresolved**; a wrapper or broker replay marker alone cannot supply it.
- The September worker records show a 1-OCPU/8-GB A1 worker alongside a
  1-OCPU/4-GB OmniRoute VM, a public subnet, pinned synthetic launcher and
  restricted transport. Those are historical observations, not current cloud
  state. WO-164's EUR 1.85 boot-volume estimate explicitly excluded tier unit
  pricing and proved neither a charge nor a zero-cost outcome.

## Recommended dependency order, subject to owner decision

1. **Local deployment bridge work order.** Add a reviewed, explicitly opt-in,
   fixed-pin pilot broker entrypoint/configuration and surgical installer and
   rollback that preserve the working synthetic broker, forced-key identity,
   sudoers and administrative SSH. No default pilot enablement, worker contact,
   candidate transport or QueueItem mutation. Test pin/owner checks, install
   refusal, targeted restoration and synthetic compatibility; independently
   review before any installation. This step remains local-only.
2. **Separate attempt-authority architecture and implementation.** The CSA must
   define a canonical, durable pre-dispatch claim for an identified QueueItem,
   request ID/nonce/Artifact digests and `UNKNOWN` recovery across process
   restarts and competing dispatchers. Reconcile that contract with the existing
   queue lifecycle/storage and OWNER-DECISION-036's response-only result meaning;
   do not quietly repurpose `QueueItem.result` or add a duplicate job registry.
   Obtain the necessary owner decision, then implement and independently test a
   one-shot controller operation. A fresh request for the same unresolved item
   must fail closed; SSH loss must not cause automatic retry or overwrite.
3. **Fresh read-only go/no-go.** Verify the account's current tier, home region,
   actual A1 allocations, combined boot/block storage, billing/usage and
   resource charges. Verify the worker's present identity, CPU/memory, OS,
   Docker/runtime/cgroup support, pinned cached image and installed file hashes;
   administrative and restricted-key continuity; exact SSH source CIDR; and
   whether the rule is shared at subnet level. Record only redacted evidence.
   Historical screenshots, cost previews and September checks are insufficient.
   No new billable resource, account upgrade, image pull, network ingress or
   software install is part of this go/no-go.
4. **Separate live authorization.** Identify the exact canonical candidate and
   acceptance Artifact IDs/digests and their origin. Review the acceptance
   script for actual invocation and assertions against the candidate. The
   current launcher runs the acceptance script and candidate in one Python
   process; even apparent invocation plus zero exit does not prove candidate
   quality (the candidate can terminate the process). The first pilot may prove
   only bounded transport/execution. A stronger validation claim needs a
   separately reviewed child-process harness and negative control. Set an
   explicit cost ceiling and rollback owner. Only then seek approval for a
   timed, targeted upgrade and exactly one request. If any pin, entitlement,
   SSH continuity or cleanup condition is uncertain, stop without dispatch.
5. **Bounded live attempt, only if approved.** Arm a recovery timer before
   mutation; install exact reviewed bytes while preserving the previous
   transport; verify hashes, ownership, runtime policy and both SSH paths;
   dispatch one request without retry; validate the correlated response; inspect
   exact owned staging/container residue; and record bounded evidence in the
   originating QueueItem. An `UNKNOWN` transport result or `cleanup_failed`
   quarantines further admission pending authenticated status/cleanup inspection.
   Restore only the pilot change if installation or continuity fails. Do not use
   a broad Docker prune or the full transport rollback as routine pilot cleanup.

## Security, cost and evidence constraints

The existing pilot launcher requests `runsc`, `--pull=never`, no container
network, a read-only root, fixed non-root UID, 1 CPU/1 GiB, bounded processes,
output and time, and exact cleanup. Local tests prove command construction, not
that the current ARM64 worker enforces the policy. A Docker or gVisor downgrade
is not an acceptable workaround. The candidate must not receive the Docker
socket, host credentials, QAOS repository or provider state. No shared security
list change is implicit: OCI security lists affect a subnet and can affect
OmniRoute; network changes require their own scope and impact proof.

Oracle's current public documentation describes A1 Always Free as 1,500
OCPU-hours and 9,000 GB-hours per month (equivalent to 2 OCPUs/12 GB), home-region
only, with a combined 200-GB boot/block allowance and possible idle reclamation.
It does not establish this account's present tier, allocations, charges or
continued availability. Trial-end overprovisioning can be disabled/deleted;
budgets are soft alerts, not a hard spending stop. Any claim of "free" therefore
requires fresh account-specific evidence and an explicit owner spending decision.

Primary-source references checked 2026-10-04:

- Oracle Always Free: <https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm>
- Oracle Free Tier: <https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm>
- Oracle budgets: <https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/budgetsoverview.htm>
- Oracle network security: <https://docs.oracle.com/en-us/iaas/Content/Security/Reference/networking_security.htm>
- Docker create/no-pull: <https://docs.docker.com/reference/cli/docker/container/create/>
- Docker resource limits: <https://docs.docker.com/engine/containers/resource_constraints>
- gVisor installation and security limits: <https://gvisor.dev/docs/user_guide/install/> and <https://gvisor.dev/docs/architecture_guide/security/>

## In scope, verification and stop

In scope: repository/source/control-plane and official-document inspection,
this design record, DECISION-REQUEST-023, and state/verification handoff.
Non-goals: product or worker code, tests, model calls, candidate creation,
credential access, SSH/OCI/Docker changes, deployment, QueueItem mutation,
generated-code execution, promotion or model designation.

Verify the decision record against the local contracts and historical worker
evidence; parse state JSON, check whitespace and obtain independent review.
Then STOP for the owner selections in DECISION-REQUEST-023. Approval of those
selections would authorize only the next **local deployment-bridge
implementation**; attempt-authority design/implementation, fresh read-only
preflight and one live attempt remain separate gates.
