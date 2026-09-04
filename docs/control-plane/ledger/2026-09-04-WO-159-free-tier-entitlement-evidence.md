# WO-159 — Free-Tier Entitlement Evidence and Operational Baseline

2026-09-04; baseline `bb2b261`; `feat/operational-builder-chain`.
Authority: owner requires certainty about what survives the trial and what QAOS can
comfortably use, supported by Oracle's own statements. Objective: reconcile the
apparently conflicting A1 figures by account state and establish the conservative
post-trial baseline. Scope: official Oracle sources, signed-in Console evidence and
control-plane records only. No resource or account change. Status: COMPLETE.

## Evidence hierarchy

Oracle describes its cloud contract model as agreement plus ordering document plus
service policies. The Cloud Services Agreement incorporates service descriptions
and program documentation and permits Oracle to update service specifications on
its websites. Marketing summaries and the Console are useful corroboration, but do
not override the account-specific Free Tier documentation.

Official sources retrieved 2026-09-04:

1. Oracle Cloud Infrastructure Free Tier, updated 2026-06-29:
   https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm
2. Always Free Resources:
   https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
3. Arm-Based Compute:
   https://docs.oracle.com/en-us/iaas/Content/Compute/References/arm.htm
4. Oracle Cloud Free Tier FAQ:
   https://www.oracle.com/cloud/free/faq/
5. Oracle PaaS and IaaS Global Price List, current retrieval:
   https://www.oracle.com/in/a/ocom/docs/corporate/pricing/oracle-paas-and-iaas-global-price-list.pdf
6. Oracle cloud contract model:
   https://www.oracle.com/contracts/cloud-services/

The signed-in account Console also supplied the account banner, quota, shape labels,
subscription state and live inventory recorded in WO-157 and WO-158.

## Reconciliation

The current Arm-Based Compute page, Global Price List and this tenancy's Console
banner show the first 3,000 A1 OCPU-hours and 18,000 GB-hours per month as free. The
current Free Tier guide is more specific about the state after a trial: an Always
Free tenancy must have no more than 2 OCPUs and 12 GB total across all A1 instances.
It warns that excess A1 instances are disabled and later deleted unless the account
is upgraded. The Always Free Resources page expresses the same allowance as 1,500
OCPU-hours and 9,000 GB-hours per month.

Therefore the safe, receipt-backed interpretation for this free-only account is:

- during the active trial, broader A1 use can consume promotional/trial entitlement;
- after the trial, durable Always Free A1 is 2 OCPUs and 12 GB total;
- the 3,000/18,000 price-list row must not be used to promise a free-only post-trial
  allowance when Oracle's account-state-specific guide says 2/12;
- a future Oracle support response or account ordering document can improve this
  evidence, but cannot safely be presumed.

This is a conservative operational conclusion, not legal advice. It is designed to
avoid dependence on the more generous reading while Oracle's published surfaces
remain inconsistent.

## What this tenancy can durably use

| Resource | Oracle Always Free baseline | Current use | Defensible remainder |
| --- | --- | --- | --- |
| A1 Flex | 2 OCPUs / 12 GB total after trial | OmniRoute: 2 OCPUs / 12 GB | None |
| E2.1.Micro | Up to 2 instances | 0 | 2 instances |
| Boot/block storage | 200 GB aggregate | OmniRoute boot: 47 GB | About 153 GB aggregate |

The storage remainder is arithmetic from observed allocation, not a reservation or
billing guarantee. Network, egress and other service limits require their own
manifest controls.

## Comfortable-use conclusion

The two Micro instances are durable free capacity, but each provides only 1 GB RAM
and subcore CPU. Current Oracle documentation does not support a guaranteed burst.
They are reasonable for low-throughput helpers such as a health endpoint, tiny
control-plane service, lightweight queue/relay, monitoring agent, or deliberately
small deterministic fixtures. They are not a comfortable or credible isolation
worker for arbitrary generated code, dependency installation, concurrent builds,
or representative QAOS workloads.

The existing OmniRoute A1 is the only comfortably usable durable A1 allocation and
must remain isolated as the supporting routing service. It must not absorb the QAOS
worker role. A meaningful separate A1 worker can only be a time-bounded trial
experiment or a paid resource under current evidence.

## Decision and stop condition

For planning, QAOS SHALL treat the durable zero-cost baseline as:

- OmniRoute keeps the full 2-OCPU/12-GB A1 Always Free allowance;
- up to two E2.1.Micro instances remain available for tiny supporting workloads;
- no separate durable free A1 worker capacity is available;
- no Micro instance is represented as adequate untrusted-code isolation capacity.

Option 3 remains sensible only as a separately approved trial experiment with an
absolute teardown deadline before trial expiry, verified billing/usage alarms and no
claim of durable free deployment. Creation remains unauthorized by this evidence
work order.

Verification: cross-source consistency analysis, current Console evidence from
WO-157/158, JSON parse and Git whitespace checks. No product or infrastructure
changed. Stop after establishing the conservative operational baseline.
