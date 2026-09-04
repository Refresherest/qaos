# WO-157 — Oracle Console Manifest Inspection

2026-09-04; baseline `9db7e2b`; `feat/operational-builder-chain`.
Authority: owner authorized read-only Oracle Console inspection and public-terms
research. Objective: capture tenancy-visible Micro/A1 launch evidence and identify
remaining zero-cost launch gates. Scope: form previews and control-plane records
only. No instance, network, key, volume, quota request, upgrade, trial-credit use,
software installation, deletion, or OmniRoute change was authorized or performed.
Status: COMPLETE / launch remains blocked by an entitlement contradiction and
unresolved manifest controls.

## Tenancy-visible evidence

The signed-in Create compute instance form in `af-johannesburg-1` showed:

| Candidate | Console evidence |
| --- | --- |
| Micro | `VM.Standard.E2.1.Micro`, `Always Free-eligible`; 1 core OCPU, 1 GB memory, 0.48 Gbps; compatible image `Canonical Ubuntu 24.04 Minimal`, build `2026.08.25-0`, price `Free`, Shielded instance |
| A1 | `VM.Standard.A1.Flex`, `Always Free-eligible`; default draft 1 OCPU, 6 GB memory, 1 Gbps; compatible image `Canonical Ubuntu 24.04 Minimal aarch64`, build `2026.08.25-0`, price `Free` |

Selecting the ARM image while Micro was active produced an incompatibility warning
and reset the shape to A1. This confirms architecture-specific image selection; it
does not designate A1 or approve a launch.

Both shape previews showed an estimated boot-volume line and total of EUR 1.85 per
month. The same panel explicitly said the estimate does not reflect tier unit
pricing. Therefore the preview is neither evidence of a charge nor a zero-cost
guarantee. The inspected draft was never submitted. Leaving the draft crashed the
embedded browser; no final Create action occurred.

Prior owner-supplied account evidence remains:

- regional A1: limit 16 OCPUs, usage 2, available 14; memory limit 96 GB, usage
  12 GB, available 84 GB;
- AD-1 Micro: active limit 2, usage 0, available 2;
- existing `qaos-omniroute`: A1 Flex, 2 OCPUs, 12 GB, running;
- one 47 GB OmniRoute boot volume and no separate block volumes;
- Johannesburg home region and no other owner-created resources.

Quota availability is capacity evidence, not billing entitlement or designation.

## Material Oracle-source contradiction

The account's Instances banner and Oracle's current Arm-Based Compute page describe
3,000 A1 OCPU-hours and 18,000 GB-hours per month, equivalent to 4 OCPUs and 24 GB.
The Oracle Free Tier/Always Free guide describes 1,500 OCPU-hours and 9,000 GB-hours,
equivalent to 2 OCPUs and 12 GB. The existing OmniRoute instance already consumes
2 OCPUs and 12 GB. The price list also scopes its 3,000/18,000 statement to paid
tenancies. These statements do not safely establish that a second A1 remains free
after the trial.

Sources inspected:

- https://docs.oracle.com/en-us/iaas/Content/Compute/References/arm.htm
- https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm
- https://www.oracle.com/cloud/price-list/

The Free Tier guide also states that two E2.1 Micro instances and an aggregate
200 GB of boot/block storage are Always Free in the home region. Oracle can reclaim
idle A1 instances under documented utilization criteria.

## Correction to prior evidence

WO-154's description of Micro as 1/8 OCPU "with bursting" is not supported by the
current Burstable Instances documentation. Oracle states that subcore Micro
instances cannot burst, and burst capacity generally is not guaranteed. Treat
Micro as fixed, highly constrained capacity for the bounded tiny-fixture experiment.
This correction does not rewrite WO-154's historical record.

Source: https://docs.oracle.com/en-us/iaas/Content/Compute/References/burstable-instances.htm

## Manifest consequences and stop condition

- The public July image candidate in WO-156 is superseded for selection purposes
  by the tenancy-visible `2026.08.25-0` builds. Exact regional OCIDs remain unresolved.
- Micro uses the x86-64 image/runtime path; A1 requires aarch64 artifacts. Neither
  route is designated while the launch decision remains open.
- The gVisor archives have publisher checksums only; archive bytes remain
  undownloaded and unverified.
- Exact network CIDRs/rules, administrative source `/32`, dedicated SSH public-key
  reference, rootfs provenance/digest, and an enforceable cost/teardown guard remain
  unresolved.

No launch is approved. Safe next owner choices are: authorize continued Micro
manifest preparation; pause until Oracle clarifies post-trial A1 entitlement; or
separately authorize a trial-only A1 experiment with an explicit teardown deadline
and spend guard. Each is a new bounded decision. OmniRoute remains separate and
untouched.

Verification: record inspection, JSON parse and Git whitespace check only; no
runtime suite is applicable. This work order stops at read-only evidence capture.
