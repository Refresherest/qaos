# WO-154 — Micro Worker Suitability (Design Only)

2026-09-04; baseline f264ab0; feat/operational-builder-chain.
Authority: owner requested design-only Micro suitability check, then said Proceed.
Objective: assess a reduced separate worker without provisioning or changing
QAOS-OmniRoute. Scope: design and control-plane evidence only. Non-goals: spending,
trial-credit consumption, installs, credentials, remote commands, product changes.
Acceptance: reconcile supplied tenancy evidence, compare host/workload budgets,
state admission tests and stop at a concrete next decision. No readiness claim.

## WO-153 evidence resolution

Owner-supplied Console screenshots, not independent API observations:
- Johannesburg regional A1 cores: limit 16, usage 2, available 14; memory 96/12/84.
- AD-1 active standard-e2-micro-core-count: limit 2, usage 0, available 2.
  Deprecated vm-standard-e2-1-micro-count is not an extra allocation.
- Subscription displayed EUR250 remaining, zero reported usage, 16/30 days left.
  Trial credits and service quota are not durable free entitlements.
- Root boot-volume list: only qaos-omniroute, 47 GB, VPU10, no backup policy.
  Root block-volume list empty. Owner confirms Johannesburg is home region and
  no other resources/compartments created except QAOS-OmniRoute.

WO-153 read-only assessment is complete with a conditional Micro proposal, not
a launch guarantee. Public Always Free terms support two Micro instances and
200 GB combined boot/block storage. Arithmetic: 200 - 47 = 153 GB potentially
remaining; a provisional 50 GB worker gives 97 GB combined, 103 GB remaining.
Recheck exact image minimum, eligibility and performance settings before launch.
Oracle's page inconsistently mentions 47 and 50 GB minimums; use 50 GB as planning
budget, not a verified image minimum. No paid backups/replicas/storage tiers assumed.
The existing A1 allocation matches the published 2 OCPU/12 GB allowance; do not
use larger quota or temporary trial credit as proof of a second free A1 worker.
[Oracle Always Free](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)

## Suitability conclusion

Conditional candidate for a tiny validation experiment; NOT suitable as the
unchanged WO-151 worker, general QAOS build host or production service.
Micro supplies AMD/x86-64, 1 GB RAM and 1/8 OCPU baseline with bursting. WO-151
proposed ARM64, 2 GiB host RAM and 1 GiB candidate RAM: that candidate alone cannot
fit with OS/runtime overhead on Micro. Two Micro instances do not pool RAM.
Do not depend on CPU bursts to meet deadlines. No GPU, model inference, browser,
package compilation or full repository regression suite on this worker.

Proposed reduced experiment (owner approval required): one standard-library-only
Python fixture at a time; candidate 128 MiB memory, 16 processes, 16 MiB scratch
charged within that memory budget, 256 KiB output per stream, 30-second wall cap.
Retain WO-151 bounded manifest/immutable-input design, restrict fixture total to
1 MiB, and cap candidate CPU at 0.1 CPU pending actual guest topology measurement.
These are refusal ceilings, not measured requirements or guaranteed performance.
Host admission must measure total guest memory and idle OS/runtime consumption;
reserve at least 256 MiB headroom after candidate and measured runtime overhead.
No swap-based capacity claim. Refuse on insufficient memory, OOM, slow deadline,
missing controls or cleanup failure; never relax isolation to make it fit.

Runtime remains unselected. Evaluate an x86-64 isolation runtime (gVisor is one
candidate) on the separate host; documentation alone proves neither RAM overhead
nor enforcement. Keep management credentials outside candidate reach, deny all
candidate network including metadata and OmniRoute, no privileged mounts/socket,
read-only inputs, independent verdict collection, bounded output/process tree,
and verified whole-worker reset/disposal after untrusted work. A separate VM alone
does not prevent credential theft or network abuse inside the guest.
[gVisor security model](https://gvisor.dev/docs/architecture_guide/security/)

Keep durable source/evidence outside disposable storage. Existing
src/qaos/capabilities/python_project.py is Windows/NTFS trusted publication with
ordinary subprocess execution, not a Linux sandbox transport; do not deploy the
whole QAOS checkout or reinterpret its success as worker acceptance.

## Next decision and stop

Recommend a design-only setup specification for ONE Micro experiment: exact
eligible x86-64 image, pinned runtime, separate network/admin identity, cost guard,
trusted management location, bounded harmless calibration and independent negative
tests, teardown by exact owned IDs. It must address idle-resource reclamation and
recreation availability; disposable does not mean instant reprovisioning.
Obtain separate explicit provisioning approval after that specification. If it
cannot satisfy the memory/security gates, stop for a host/budget decision. No
co-resident, laptop or paid fallback; never resize or restart OmniRoute.

Verification: documentation-only JSON/whitespace checks; source boundary inspected.
No runtime tests, deployment, capacity reservation or independent review claimed.
Existing dirty skills/untracked files preserved. Architecture-awareness retained
product authority and isolation gates despite reducing workload budgets.
Rollback is record revision only. WO-154 design assessment complete; stop here.
