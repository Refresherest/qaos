# WO-151 — Separate Cloud Worker Design

2026-09-04; baseline f3626e6; feat/operational-builder-chain.
Authority: owner proceed on HANDOFF-130 and explicit project-separation direction
(OWNER-DECISION-033). Design/records only; stop for owner approval. No deployment,
remote mutation, provisioning, runtime install, candidate execution or spending.

## Baseline and ownership

VERIFICATION-120 observed a healthy OmniRoute container on the existing Oracle
ARM64 VM (2 CPUs, about 12 GiB RAM, 39 GiB free disk). These are prior snapshots,
not today's capacity guarantee. Ordinary runc/Docker was present; no enhanced
worker isolation or spare tenancy quota was established. Preserve that service.

| Domain | Authority / boundary |
| --- | --- |
| Main QAOS | Product contracts, approved requirements/tests, model governance, canonical objectives/tasks and retained evidence. |
| Supporting QAOS-OmniRoute | Routing service and its credential-bearing deployment; changes require supporting-project scope. |
| Proposed execution worker | Resource supporting QAOS validation, accessed through a bounded job interface; cannot own product decisions or routing credentials. |
| Operator | Infrastructure approval, budgets and promotion decisions; a job verdict grants neither deployment nor model designation. |

Do not create a duplicate QAOS product checkout under OmniRoute deployment, place
candidate files in /opt/omniroute, mount its database/secret directory into workers,
or stage its configuration into this repository. Existing supporting repository
location/ownership was not inspected; do not invent it or move files. Main-repo
records here describe dependency contracts, not a takeover of the supporting project.

## Option A — Separate worker VM (recommended target)

Keep the current qaos-omniroute instance dedicated to existing routing work. Use
a distinct worker instance/resource identity with separate volumes, administrative
credential and network policy. No route to OmniRoute, host credentials or OCI
metadata from candidate execution. Cloud management credentials stay outside the
candidate guest; narrowly scoped management ingress is not candidate egress.

For the initial gate, use reviewed ARM64-compatible runtime/image and one job at
a time. Proposed candidate caps: 1 CPU, 1 GiB RAM, 32 processes, 30-second job
deadline, 256 MiB scratch, 1 MiB per output stream. Host runtime overhead is additional;
provisional worker host envelope 1 CPU/2 GiB RAM and up to 20 GiB total disk must
be checked against actual OCI shapes/minimum boot-volume sizes before approval.
These are design targets, not a promise that OCI can provision that combination.
Boot deadline proposed 120 seconds; terminate/refuse on unresolved cleanup.

Prefer worker host disposal/reset between untrusted jobs, not merely deleting a
container's directory. Any reusable base is immutable and verified by digest;
results/source are retained outside disposable resources. Capacity, boot time,
cost and a supported resource-isolation runtime remain admission gates. Existing
Windows/NTFS trusted builder remains unchanged; this is a separate future capability.

Do not assume the existing 2-CPU/12-GiB allocation leaves another free instance.
Read-only tenancy limits/usage and proposed boot-volume charges must be checked
before a launch request. Do not shrink or migrate OmniRoute to free capacity.
If no approved zero-cost capacity exists, stop and request a budget/host decision.
Oracle documents entitlement conditions and possible idle-resource reclamation;
durable backups and reconstruction are required, not optional worker-local state.
[Oracle Always Free](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)

## Option B — Enhanced co-resident interim worker (not selected)

Would use a distinct execution identity/runtime/data root and explicit limits on
the current VM; never OmniRoute's container/Compose project, secrets or Docker socket.
Candidate isolation such as gVisor requires ARM64/kernel/workload evaluation and
verified enforcement. Different container names do not create a host boundary.
Shared CPU/disk/kernel/control paths remain a blast-radius and availability risk.
Docker warns that container capabilities/mounts and kernel vulnerabilities can
limit isolation; gVisor has its own documented threat model and limitations.
[Docker security](https://docs.docker.com/engine/security/),
[gVisor security model](https://gvisor.dev/docs/architecture_guide/security/)

One concurrent candidate capped at 1 CPU/1 GiB plus runtime overhead is a proposed
ceiling, not verified headroom. The existing small host cannot promise interference-
free service. No daemon default-runtime change, auto-configuring package install,
restart/reload or OmniRoute limit changes without an explicit supporting-project
maintenance work order. Option B requires an affirmative risk decision; it is not
the fallback when Option A quota is unavailable. No untrusted workload now.

## Proposed transfer and validation protocol (both options)

QAOS's approved objective/task identifies one immutable candidate manifest and a
separately authored acceptance bundle. Stage only allowlisted relative regular
files with count/size/digest limits; reject links, traversal, duplicate names and
unexpected archive members before transfer. Do not clone the whole product repo,
copy .git/.env or route credentials, or accept a candidate-supplied shell command.
Initial input budgets: 32 files, 1 MiB/file, 8 MiB total; exact schema requires
later implementation approval. No runtime dependency download during a job.

Trusted management transfers these bounded inputs to a per-job staging location
before candidate launch. Candidate sees read-only input and acceptance mounts,
read-only base filesystem and quota-limited scratch; no host/home/socket mounts,
no capabilities, no privilege escalation or network. Runtime checks enforce this,
not the candidate. A separately approved harness owns fixed test entrypoints.

Harness output is framed, length-bounded and drained with caps enforced while
produced. Treat every returned byte as untrusted; parse the approved schema, match
job/input/test/image digests and validate paths/sizes before durable ingestion.
Never mount writable main-project data into the guest or deserialize executable
objects. An administrative broker may collect output only via a restricted channel;
it must not expose its credentials/socket to candidates. Exact broker/runtime APIs
and fixture isolation are implementation stop conditions, not completed controls.

QueueItem.result retains correlation/verdict/bounded diagnostics and independently
observed termination/cleanup evidence under QAOS authority. Artifact ownership
retains approved bytes/provenance; no new parallel registry is introduced here.
Approval/promotion stays outside the guest. Candidate self-reported test success
alone is insufficient, especially if it can tamper with the harness or tests.

## Enforcement and operational gate

Require VERIFICATION-119's independently authored network/credential/filesystem,
resource/process/output/deadline/reset/tamper tests. First run a harmless known
fixture only after separate setup approval; then reviewed bounded negative tests.
No uncontrolled exhaustion, public network probing or real-secret canaries.

Stop admission on policy mismatch, missing limits, unknown image digest, low disk,
or cleanup failure. Cancel the entire job/process tree; quarantine worker identity
until disposal is verified. Do not return success after a cleanup error. Removal
targets exact owned job/instance/volume IDs only; never broad image/volume pruning.
Durable evidence must survive deletion. If collection fails, report incomplete
evidence rather than retrying or promoting automatically.

Setup impact/rollback: A requires new scoped cloud resources, verified image and
management policy, potentially chargeable; no existing-instance restart planned.
Before launch record exact resource IDs, approved limits and removal procedure.
Rollback stops jobs and removes only new approved disposable resources, retaining
evidence; it never deletes/resizes OmniRoute. B may affect its host runtime, so
requires a separate maintenance/backup/restore window and is not approved here.
No installation commands are supplied until the selected runtime, pin and effects
are reviewed. No zero-risk or production-readiness claim.

## Decision requested / next bounded step

Approve A as the target and authorize only a read-only OCI tenancy capacity/cost
check for a separate worker, or explicitly select B for further risk/setup design.
A selection does not authorize provisioning, spend, quota requests or resizing.
If access is unavailable, ask for the relevant redacted Console limits/usage view;
never request API secrets. No fallback to laptop or shared ordinary Docker.

Verification: source-of-truth boundaries reconciled with OWNER-DECISION-033 and
existing Artifact/QueueItem/intent contracts from prior inspection. No product,
tests, services or active data changed. Official sources inform design only, not
configured-control proof. JSON/whitespace checks apply; no runtime tests rerun.
Architecture-awareness kept supporting infrastructure distinct from product authority.
Preserve unrelated dirty skills/configuration/drafts/tools/test folders. Rollback
is owner-directed record revision. Stop at decision.
