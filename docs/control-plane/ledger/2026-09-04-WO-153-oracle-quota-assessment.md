# WO-153 — Read-only Oracle Quota Assessment

Resolution: owner supplied Console evidence and home-region/inventory confirmation;
see WO-154 for reconciled observations and conditional Micro proposal. Assessment
complete; historical blocker below is resolved, not a provisioning approval.

2026-09-04; baseline 4f8ca95; feat/operational-builder-chain.
Authority: OWNER-DECISION-034 and owner proceed on HANDOFF-132.
Objective: establish whether a separate worker fits actual tenancy compute and
storage entitlements without changing OmniRoute or incurring spend.
Scope: read-only access discovery, official documentation and control-plane records.
Non-goals: provisioning, credential configuration, quota requests, billing changes,
remote installation, resizing, product changes or untrusted execution.

## Evidence and blocker

Get-Command oci returned no command; Test-Path for the standard user .oci/config
returned False. This establishes only absence of the normal local CLI/config path,
not absence of all possible account access. No authenticated tenancy API access is
established. No credential files, environment values or SSH private keys were read.
VERIFICATION-120 supplies prior guest inventory, not tenancy quota or billing data.
No remote commands or Console actions were performed in this assessment.

Oracle's current public documentation describes 2 OCPUs/12 GB for Always Free A1,
200 GB combined boot/block storage, and a 47 GB minimum boot volume. These public
figures do not establish this account's entitlement, current allocations, regional
physical capacity or charges. The proposed 20 GiB total worker disk envelope must
be revised for an OCI image's actual minimum; it is not a feasible approved size.
[Always Free documentation](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)

Status: BLOCKED pending redacted tenancy evidence. No exact feasible shape or
zero-cost claim. Service limits alone are not a free-tier allowance or a physical
capacity reservation. Do not shrink OmniRoute or fall back to co-residency.

## Required evidence / acceptance

Request Console Limits, Quotas and Usage for Compute in the intended region:
A1 core/memory and E2 Micro rows, with limit, usage, available values and scope.
Also need home region/account tier (no identifiers), existing instance shape and
allocation, all boot/block volume allocations including unattached volumes across
relevant compartments, and applicable free entitlement/cost evidence. Verify
prospective image boot size and storage performance tier before a setup proposal.
E2 Micro is not an automatic substitute for the proposed ARM64/2 GiB worker.
[Viewing tenancy limits](https://docs.oracle.com/en-us/iaas/Content/General/service-limits/view-tenancy.htm)

Stop for those inputs; then resume this work order to produce a cost/capacity
proposal or explicit budget blocker. No new resources authorized in either case.

Verification: architecture_inspect.py inspected 200 Python files; reported static
findings remain outside this documentation scope and are not repaired. JSON parse
and Git whitespace checks apply to records; no runtime regression rerun warranted
for documentation only. Existing modified skills and untracked material preserved.
Recovery: owner-directed record correction, not infrastructure rollback.
