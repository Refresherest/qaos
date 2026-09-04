# WO-160 — OmniRoute Minimum Capacity Assessment

2026-09-04; baseline `cc42cc9`; `feat/operational-builder-chain`.
Authority: owner requested a double-check of the 2-OCPU/12-GB allowance and an
evidence-based split that gives QAOS the bulk if a smaller OmniRoute allocation is
sufficient. Objective: establish a candidate minimum and proof gate. Scope: official
Oracle documentation and prior verified read-only host/routing evidence. No resize,
restart, resource limit, load generation, provider calls or infrastructure change.
Status: COMPLETE assessment / allocation change NOT approved or proven.

## Entitlement recheck

Retrieved 2026-09-04, Oracle's current Free Tier page explicitly says that after the
trial an Always Free user must have no more than 2 OCPUs and 12 GB total across all
A1 instances. The detailed Always Free page independently states 1,500 OCPU-hours
and 9,000 GB-hours, equivalent to 2 OCPUs and 12 GB. It also permits one or two A1
instances and describes the allocation as flexible.

- https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm
- https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- https://docs.oracle.com/en-us/iaas/Content/Compute/References/computeshapes.htm

The A1 shape requires at least 1 OCPU per instance and at least 1 GB memory. With a
two-instance design under the post-trial allowance, CPU cannot be weighted toward
QAOS: each VM must receive 1 OCPU. Only the 12 GB memory pool can be weighted.

## Evidence about OmniRoute

VERIFICATION-120 observed the live 2-OCPU/12-GB Ubuntu host before this assessment:

- total host use: 1,498 MiB; 10,428 MiB available; no swap;
- OmniRoute container: 835.9 MiB, 0.00% CPU in the sample, 21 PIDs;
- Docker, AppArmor and the OS account for the remainder;
- OmniRoute was healthy after eight days and was the only running container;
- container memory, CPU and PID limits were unset;
- three normal QAOS role routes later completed through OmniRoute, but no forced
  fallback, concurrency, soak, or peak-load test was performed.

This proves a quiet steady-state footprint and functional routing, not a production
peak. The current SSH private-key location could not be rediscovered without exposing
or moving secrets, so no new host snapshot was fabricated. OCI historical metrics
were not captured in this work order.

## Candidate split

| Service | Candidate allocation | Rationale |
| --- | --- | --- |
| QAOS-OmniRoute | 1 OCPU / 4 GB | Minimum CPU for a separate A1 VM; about 2.7x the observed whole-host memory use and about 4.8x the observed container use; preserves OS/Docker headroom without swap |
| QAOS worker | 1 OCPU / 8 GB | Receives two-thirds of memory and the only remaining OCPU; materially stronger than Micro, but still a small sequential worker |

The 1-OCPU/4-GB OmniRoute target is the recommended candidate minimum, not yet a
proven minimum. A 1-OCPU/2-GB allocation is rejected as uncomfortable: the observed
whole-host footprint would leave only about 0.5 GB with no swap. A 1-OCPU/3-GB split
has more room but insufficient margin for unobserved peaks, upgrades and SQLite/Docker
growth. Keeping 1 OCPU/6 GB is conservative but does not give QAOS the requested bulk.

The proposed 1/4 plus 1/8 split exactly consumes 2 OCPUs and 12 GB. A second default
boot volume would bring observed/default boot allocation to roughly 94–97 GB, within
the documented 200-GB aggregate; actual billing classification must still be checked.

## Required proof before resizing

Do not resize OmniRoute or create the QAOS A1 worker until all gates pass:

1. Capture at least seven days of OCI CPU and network metrics and guest/container
   memory high-water marks, including real QAOS routing activity.
2. Record request rate, concurrency, latency, error rate, restarts, OOM events,
   SQLite/WAL growth, PID peak and disk high-water mark without reading secrets.
3. In a separately authorized maintenance window, apply reversible container caps
   equivalent to the 1-OCPU/4-GB target and run normal-route plus controlled fallback
   and concurrency tests. Preserve provider-cost bounds.
4. Require zero OOM/restarts, stable p95 latency/error behavior, at least 1 GB guest
   available at peak, and sustained CPU headroom. If any gate fails, restore 2/12 and
   evaluate 1/6 rather than forcing the split.
5. Only after the cap test passes, approve an OCI shape resize with rollback evidence;
   then provision the separate QAOS worker under its own manifest.

Oracle may reclaim idle Always Free compute when documented CPU, network and A1
memory conditions are all below its thresholds over seven days. Do not generate
artificial load to evade reclamation; treat this as an availability risk for both VMs.

## Conclusion and stop

The durable entitlement is confirmed as 2 OCPUs/12 GB. The strongest evidence-backed
target is OmniRoute 1 OCPU/4 GB and QAOS 1 OCPU/8 GB. This is a candidate allocation,
not authorization to resize or proof of comfort under peak load. The next bounded
work is read-only metric collection and a proposed cap-test work order. Stop before
any service or infrastructure mutation.

Verification: official-source recheck, VERIFICATION-120 and prior routing-evidence
review, JSON parse and Git whitespace checks. No regression suite is applicable.
