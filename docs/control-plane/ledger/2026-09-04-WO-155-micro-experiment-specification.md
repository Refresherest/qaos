# WO-155 — One-Micro Experiment Specification

2026-09-04; baseline 6d06123; feat/operational-builder-chain.
Authority: owner Proceed on WO-154's design-only specification next step.
Objective: specify resource, isolation, acceptance and teardown gates for one
small experiment. Scope: this specification and current-state records only.
Non-goals: provisioning, spend/trial-credit use, installation, credential changes,
remote execution, product code or OmniRoute operations. No deployment approval.
Acceptance: actionable staged specification, explicit unresolved launch inputs,
bounded tests and refusal/cleanup conditions. Stop before external actions.

## Proposed resource envelope

- One VM.Standard.E2.1.Micro in af-johannesburg-1, AD-1; 1 GB host RAM.
- Ubuntu 24.04 LTS x86-64 platform image, minimal variant if available and eligible.
  Exact regional image OCID/build is UNRESOLVED; never substitute an ARM image.
- One boot volume, at most 50 GB, VPU10 with no performance auto-tuning, no backup
  policy/replication/additional disk. Reconfirm image minimum and free eligibility.
- Unique qaos-validation-micro experiment identity; separate VCN/subnet/security
  rules and SSH key, never reuse OmniRoute's deployment, key or network rules.
  No peering, NAT gateway, load balancer or new paid service. Proposed ephemeral
  public address only for narrowly restricted administrative SSH; no public app.
- One experiment session, at most 60 minutes after healthy login; no unattended
  recurring jobs or automatic recreation. Provisioning failure stops, no retries
  against other shapes/paid resources. Proposed boot deadline 120 seconds.

WO-154 records owner evidence of available Micro quota and 47 GB existing storage.
A 50 GB volume would total 97 GB, not a guarantee of billing eligibility. Before
launch, verify all line items against Always Free terms and the account preview;
nonzero or unclear cost is a STOP, not permission to consume trial credits. Trial
credit balance and zero historical usage are not spending controls. Recheck quotas
and inventory then; hardware capacity is unproven until an authorized launch.
[Oracle terms](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)

## Execution design proposed for approval

Use gVisor runsc directly with an Open Container Initiative bundle and systrap,
without Docker/containerd on this experiment host. This is a proposed selection,
not validated runtime readiness. Direct runsc is documented; Linux x86-64 and
kernel >=5.6 are prerequisites. Pin a specific official point release plus verified
SHA512, retaining every accompanying sidecar binary. No moving latest URL at
execution time. Exact release/checksum and minimal Python rootfs digest are
UNRESOLVED until a read-only artifact-selection pass; no fabricated pins.
[Direct runtime](https://gvisor.dev/docs/user_guide/quick_start/oci/),
[Installation](https://gvisor.dev/docs/user_guide/install/),
[Platform guide](https://gvisor.dev/docs/architecture_guide/platforms/).

Trusted operator control is this laptop for small SSH transfers/control and
bounded evidence only, not workload execution or image compilation. This is an
interim control arrangement, not the eventual cloud orchestration service. Keep
OCI management credentials outside the guest and do not attach instance-principal
permissions. New SSH private key remains outside repository/worker; no forwarding.
Verify worker host fingerprint by trusted Console evidence before SSH. A mismatch
stops. No new control plane hosted on OmniRoute.

After separately approved setup, stage verified runtime/rootfs and harmless fixture
before sealing egress. No package installation during candidate execution. Worker
network rules allow SSH only from the approved operator address; remove broad
default ingress/egress in the NEW network only. Account for additive rule sets.
Candidate additionally has no external network interface/routes or DNS, no access
to metadata, host mounts, SSH files, sockets or privileged devices. Validate guest
namespace/runtime policy and outer firewall independently; VCN isolation alone
does not establish metadata denial. No live probes against OmniRoute or secrets.

Trusted root-owned launcher accepts only a reviewed manifest and fixed entrypoint,
not arbitrary shell strings, paths or runtime flags. Execute as unprivileged UID
inside sandbox, capabilities empty, no-new-privileges, read-only root/input/test
mounts. Maximum 32 regular relative files, 1 MiB aggregate; reject links, traversal,
duplicate paths, mismatched hashes and unknown fields before staging. No repo clone.

Preserve WO-154 candidate limits: 128 MiB including 16 MiB scratch, 16 guest
processes, 0.1 CPU, 30 seconds, 256 KiB each stdout/stderr. Runtime overhead must
be measured and bounded in an outer cgroup with all descendants accounted for;
guest process limits cannot be inferred from host thread counts. The exact runsc
mapping and launcher implementation must be reviewed before any candidate run.
Reserve >=256 MiB host memory headroom after measured overhead and candidate cap;
no swap assumption. If limits cannot be enforced in this release, reject the host.

## Ordered acceptance tests (not executed)

| Gate | Bounded test | Required evidence / refusal |
| --- | --- | --- |
| Identity and cost | Inspect exact image, resource IDs, scope, eligibility and network rules | Signed-off manifest before Create; any unresolved field stops |
| Host calibration | OS/kernel/architecture, memory, cgroups; runtime version/hash; empty sandbox then tiny stdlib fixture, three sequential runs | Known expected output; no OOM; headroom >=256 MiB; each finishes within 30s |
| Input boundary | Synthetic traversal/link/hash/unknown-field manifests | Rejected before execution; no file outside task staging touched |
| Filesystem and identity | Try writing test/input/root; read synthetic host canary; inspect UID/caps/mounts | Writes/host read denied, canary absent; no real credential fixture |
| Network | Inspect namespace/routes/firewall; bounded socket attempts toward documentation-only test destinations; review explicit metadata deny | No external packets via trusted observation; timeout alone is insufficient; no actual metadata credential fetch |
| Memory/process/scratch | Individually bounded reviewed fixtures attempt just beyond each cap, under outer guard | Expected rejection/termination; host remains responsive; no host-wide exhaustion |
| Output/deadline | Emit at most cap+1 bytes per stream; finite 35s sleep; small finite child tree | Launcher terminates at output cap or 30s plus <=5s cleanup; no surviving descendants |
| Result integrity | Wrong job/digest, malformed/oversized JSON and fake success fixtures | Trusted collector rejects; candidate success alone never promotes |
| Disposal | Collect evidence, terminate exact VM and delete its boot volume/new network dependencies | Console/API confirms absence, no retained job state; no broad pruning |

All tests require reviewed executable fixtures/launcher in a later implementation
WO. No fork bomb, unbounded allocator or uncontrolled flood. Supervisor must retain
resources outside candidate cgroup; on lost SSH or missing evidence, mark FAILED /
UNKNOWN and use independent Console termination, never report success. Candidate
results are untrusted; collect bounded hashes/exit/termination evidence outside
guest, use existing Artifact/QueueItem semantics only in later integration.

## Cleanup and approval gates

Record exact created VM, boot volume, VNIC/public address, VCN/subnet/gateway/rule
IDs and owner tags before tests. Cleanup authority must be explicit in launch WO.
Delete only these resources in dependency order after bounded evidence collection;
verify boot volume deletion separately. No snapshots by default. Preserve main
QAOS records; never touch OmniRoute IDs. If cleanup fails, report exact survivors
and stop admission. Dispose after negative-test session; no reuse for real jobs.
Recreation may lack capacity; idle reclamation is not a cleanup strategy.

Design specification delivered, but NOT launch-ready: image OCID/build, runtime
release/checksum, rootfs digest, operator source IP/public key reference, full
network manifest and cost preview remain unresolved. No fake exactness or inferred
approval. Next bounded work: read-only launch-manifest preparation to resolve these
fields, followed by owner approval for creation/setup/harmless tests/cleanup. Real
generated-code execution remains a separate gate even after a successful fixture.

Verification: JSON parse and whitespace checks; same-agent design inspection only.
No runtime tests, installed-control evidence or independent review claimed. Dirty
skills and unrelated untracked files preserved; no product/active-data changes.
Architecture-awareness preserved isolation and split design from launch authority.
Rollback: record revision only. Stop at the unresolved pre-launch hold point.
