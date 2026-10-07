# WO-179 — Read-Only Live Pilot Go/No-Go Preflight

2026-10-07; baseline `cce42c1` on `feat/operational-builder-chain`.
Authority: the owner's “Proceed” after WO-178's local-only ACCEPT, interpreted
as the next bounded, read-only evidence checkpoint in WO-175 and
DECISION-REQUEST-023 option 3A. Status: IN PROGRESS — account and worker
evidence incomplete; no live authorization.

## Objective and architectural context

Refresh the account, resource, network, worker, runtime, cleanup and cost
evidence needed to decide whether a separately authorized one-request
`python-single` pilot is even eligible. WO-176's bridge and WO-178's attempt
authority are local-only. Historical screenshots, cost previews and the local
test suite cannot establish present cloud state or entitlement.

The canonical candidate and acceptance Artifacts remain the payload source of
truth; the QueueItem remains the one-attempt authority. A read-only preflight
does not create a candidate, claim a QueueItem, install the bridge, designate a
model or convert a passing script into workload validation.

## In scope

- Read-only Oracle Console inspection of current account tier/trial status,
  home region, A1 allocations and shapes, all relevant boot/block volumes,
  billing/usage and cost alerts, and worker/OmniRoute placement and network
  association. Record redacted, dated values and direct Oracle documentation.
- Read-only worker inspection over the already pinned administrative SSH
  identity, **only if** the original host pin validates and key handling is
  authorized. Verify guest identity, CPU/memory, runtime pins, policy, image
  cache, deployed bridge state, SSH continuity, and owned cleanup residue.
- Compare local reviewed installer/launcher source hashes to their accepted
  pins. Identify unresolved candidate/acceptance, cost, rollback and
  cross-store lifecycle prerequisites. Reconcile control-plane state records.

## Explicit non-goals

No account upgrade, spending, resource creation/deletion/resize, VCN or guest
firewall change, software install/update, image pull, bridge enablement,
candidate transfer, generated-code execution, QueueItem claim, request send,
retry, active JSON-to-SQLite cutover, Task/Objective adjudication or model
governance transition. Do not reveal or source-control credential values.

## Requirements, verification and stop

1. Use account-specific live observations for entitlement, allocation and
   charges; label missing values **unverified**, never infer zero cost from an
   estimate or an empty historical usage chart. Oracle's current general
   Always Free guide states 1,500 A1 OCPU-hours and 9,000 GB-hours monthly,
   equivalent to 2 OCPUs/12 GB for an Always Free tenancy, and 200 GB of
   combined boot/block storage in the home region. The trial-end guide says
   excess A1 may be disabled and later deleted. These are public terms, not
   proof of this tenancy's current state.
2. Do not run worker commands unless strict host-key verification succeeds.
   Use only bounded, read-only inventory commands; no test container or
   synthetic exchange. If a temporary key copy is needed, require the owner's
   specific approval and remove it after the probe.
3. Compare expected and observed pins, account/worker/OmniRoute capacity,
   storage, network ingress and cleanup. A missing or contradictory critical
   observation yields **NO-GO / insufficient evidence**, not a guessed PASS.
4. Record exact commands, results, source dates, unresolved risks and a
   separate proposed live authorization manifest. Verify control-plane JSON
   parsing and scoped whitespace. Obtain independent review before calling
   the preflight complete. Then **STOP**: no live mutation or request without
   a new scoped owner approval.

Primary Oracle references checked 2026-10-07:

- <https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm>
- <https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm>
- <https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/budgetsoverview.htm>
- <https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/costusagereportsoverview.htm>

## Evidence so far

- The local reviewed pilot deployment script SHA-256 remains
  `37d75c567231bdbe2d0255200331345001f02704d79557897d670e81c23e37e8`;
  the local pilot launcher SHA-256 remains
  `1b8e20cbc63999244862544f5c9933fb14cf9701d22b455bb753d4ebf4a81403`.
  This does **not** verify installed worker bytes.
- Oracle's current Budget documentation calls budgets soft limits and says
  alerts are evaluated periodically, every 24 hours. Cost reports are
  generated daily. Neither is a hard, immediate spending stop; no account-
  specific cost or zero-charge conclusion follows from these public pages.
- After the owner signed in on 2026-10-07, the Console showed a Free Tier
  account whose Free Trial had ended, with South Africa Central (Johannesburg)
  selected. The root-compartment instance list showed only `qaos-worker` and
  `qaos-omniroute`, both Running as `VM.Standard.A1.Flex` in AD-1. Worker was
  1 OCPU/8 GB with public IPv4 `92.4.147.163`; OmniRoute was 1 OCPU/4 GB.
  This matches the prior intended 2-OCPU/12-GB split, but the tenancy's home
  region was not independently confirmed.
- The Compute regional `af-johannesburg-1` service-limit view, filtered for
  `a1` and root compartment, showed `standard-a1-core-regional-count`: limit
  2, usage 2, available 0; `standard-a1-memory-regional-count`: limit 12 GB,
  usage 12 GB, available 0. The instance-list banner still advertised 3,000
  OCPU-hours and 18,000 GB-hours monthly, whereas Oracle's current public
  Always Free guide states 1,500/9,000 and the Free Tier trial-end guide says
  no more than 2 OCPUs/12 GB across A1 instances. Treat the observed 2/12
  service limit and documented post-trial boundary as the conservative gate;
  do not infer an extra 2/12 from the inconsistent banner.
- The root-compartment boot-volume list showed exactly two volumes, each
  47 GB, carrying an Always Free label. Both were attached to the named
  instances; combined observed boot storage is 94 GB. The root-compartment
  standalone block-volume list showed no items. This is not an exhaustive
  cross-compartment or cross-region inventory.
- The Universal Credits subscription list showed its Infrastructure entry as
  **SUSPENDED**, with renewal date 2026-09-19 and listed commitment value
  €0.00. Its detail view retained the historical €250.00 total commitment
  value; the 2026-08-21 through 2026-10-07 usage view showed €0.00
  consumption and 5 SKUs in one region. Cost Analysis for 2026-10-01 through
  2026-10-07 showed cost-to-date 0 for Compute, Block Storage, VCN and
  Telemetry. The page warns that billing estimates may omit actual usage and
  usage data is typically delayed about 24 hours. This is evidence of the
  displayed estimate, **not** a zero-future-charge guarantee.
- The Budgets list showed no budget rows. The shared default security list
  for `qaos-vcn` still allows stateful TCP/22 ingress from `0.0.0.0/0` and all
  protocol egress to `0.0.0.0/0`, plus the two expected ICMP ingress rules.
  The worker's primary VNIC was attached to `qaos-public-subnet`; its
  private IPv4 was `10.0.0.20`. Guest firewall enforcement remains unverified.
- The Oracle session subsequently returned to a password sign-in screen.
  No login field was automated and no account setting or resource was changed.
- On a later read-only continuation on 2026-10-07, the Oracle session was
  active again. Governance & Administration > Tenancy Details showed the
  `emergestrategic` tenancy as Active and its **Home region: JNB**. This
  independently confirms the observed Johannesburg resources are in the
  home region; it does not prove an exhaustive cross-compartment inventory.
- The saved worker host-key pin exists, but the direct Windows OpenSSH probe
  refused the existing private key's broad ACL before authentication. The
  owner approved a temporary owner-only helper copy, but the command carrying
  that copy-and-cleanup operation was rejected before process creation by the
  execution environment. No helper copy was created, the original key was not
  changed, and no guest inventory was obtained. Do not work around this gate
  by weakening host-key checking or exposing key contents.
- The existing local SSH agent was checked without touching the private key:
  `ssh-add -l` returned "Error connecting to agent: No such file or
  directory" and `Get-Service ssh-agent` showed Stopped/Disabled. Thus no
  already-loaded identity is available for a keyless read-only worker probe.
  No service was started and no authentication attempt followed.
- At the start of this checkpoint, `PROJECT_STATE.json` still described
  DECISION-REQUEST-024 as open and omitted completed WO-178. It has now been
  reconciled with CURRENT_STATE and VERIFICATION-129. This bookkeeping update
  does not confer live authority or prove account/worker readiness.

## Separate live-approval manifest still required

Before any live gate, identify the exact canonical candidate and independently
authored acceptance Artifact IDs, digests and origin; review the acceptance
script's actual invocation/assertions; pin the proposed staged installer and
worker runtime/image bytes; name the QueueItem and one-attempt request identity;
set a numeric cost ceiling and rollback owner; and specify account/worker/SSH,
cleanup and `UNKNOWN` stop criteria. WO-175 and DECISION-REQUEST-023 require a
separate owner approval for that exact manifest. None is supplied here.

Current result: **NO-GO / insufficient fresh evidence**. The observed 2/12
allocation fits the conservative published post-trial A1 boundary, but current
worker runtime, installed bytes, guest firewall, cleanup and SSH continuity
remain unverified; delayed billing evidence is also outstanding. The tenancy
details now confirm JNB as the home region. This is a hold on live action, not
a conclusion that the worker is absent or the account is billable. No live
pilot request was sent.
