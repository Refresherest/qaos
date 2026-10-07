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
- A fresh Oracle Console attempt reached a password sign-in screen. Current
  account tier, billing, usage, A1 allocation, volumes and network are not yet
  observed. The owner must finish sign-in before those checks can proceed.
- The saved worker host-key pin exists, but the direct Windows OpenSSH probe
  refused the existing private key's broad ACL before authentication. The
  original key was not changed. A temporary restricted helper copy requires
  a separate owner answer; no guest inventory was obtained.
- At the start of this checkpoint, `PROJECT_STATE.json` still described
  DECISION-REQUEST-024 as open and omitted completed WO-178. It has now been
  reconciled with CURRENT_STATE and VERIFICATION-129. This bookkeeping update
  does not confer live authority or prove account/worker readiness.

Current result: **NO-GO / insufficient fresh evidence**. This is a hold on
live action, not a conclusion that the worker is absent or the account is
billable. Continue only the read-only preflight after the sign-in and key
handling gates are resolved.
