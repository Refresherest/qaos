# WO-161 — OmniRoute Seven-Day OCI Metrics

2026-09-04; baseline `c1e41ea`; `feat/operational-builder-chain`.
Authority: owner approved the next read-only proof step after WO-160. Objective:
inspect seven-day OCI metrics and determine whether the 1-OCPU/4-GB OmniRoute
candidate remains credible. Scope: signed-in Console metric reads and records only.
No resize, restart, cap, generated traffic, provider call or resource change.
Status: COMPLETE / historical-metric gate passes; cap test remains unapproved.

## Metric window and method

The instance Monitoring tab was set from its one-hour default to Last 7 days,
covering approximately 2026-08-28 through 2026-09-04 UTC. OCI `oci_computeagent`
charts were inspected with Auto interval. CPU and memory were reviewed as Mean and
then Max; CPU was also reviewed at P95. Values below are approximate chart readings,
not exported raw samples.

| Metric | Seven-day observation |
| --- | --- |
| CPU mean series | Normally about 0.7%; largest mean-series spike about 2.2% of the current 2-OCPU host |
| CPU maximum series | Commonly about 12–18%; several brief peaks about 50% |
| CPU P95 series | Normally about 1.5–2%; one interval near 11.5% |
| Memory mean | Stable near 12.3% of 12 GB, about 1.5 GB |
| Memory maximum | Generally 12–13%; brief peaks near 15%, about 1.8 GB |
| Network receive | Generally about 1 KB/s; observed peaks about 5 KB/s |
| Network transmit | Generally about 2 KB/s; observed peak about 6 KB/s |
| Load average | Generally 0.01–0.03; observed peak below about 0.06 |
| Memory allocation stalls | Zero throughout the displayed window |
| Disk read operations | Essentially zero with one displayed peak below 0.1 operations/s |

The window includes the period in which prior QAOS role-routing probes completed,
but it is not a formal concurrency or fallback load test. No guest OOM/restart or
application latency series was available from these charts. Custom logging warned
that the current Ubuntu image might not support that Console path; it was not enabled.

## Capacity inference

Moving from two OCPUs to one would approximately double CPU percentages if the same
work is runnable and otherwise unchanged. On that conservative projection:

- normal CPU P95 becomes roughly 3–4%; the exceptional displayed P95 interval
  becomes roughly 23%;
- brief maximum spikes that consumed about one full current OCPU could saturate the
  single OCPU momentarily, but the mean and p95 series show substantial sustained
  headroom;
- 1.8 GB observed maximum memory would occupy about 45% of a 4-GB VM, leaving about
  2.2 GB for growth and OS/Docker variance;
- network demand is negligible relative to the A1 1-OCPU bandwidth allocation;
- zero allocation stalls and very low load support the absence of current pressure.

For the observed gateway/router role—routing and streaming external model requests,
not running inference or generated-code workloads—the seven-day evidence supports
1 OCPU/4 GB as a comfortable candidate. It does not prove behavior during a provider
incident, retry storm, high concurrency, database maintenance, upgrade or future
traffic growth.

## Gate result and next action

WO-160 proof gate 1 passes for OCI CPU, memory, network, disk, load and allocation-
stall history. Guest/container restart, OOM, request latency/error and SQLite/WAL
high-water evidence remains incomplete because the existing private-key location
could not be rediscovered safely and no secret was requested or moved.

Do not resize yet. The next step is a separately authorized maintenance-window cap
test on the current host: preserve the 2/12 VM, temporarily constrain only the
OmniRoute container to 1 CPU and 4 GB, exercise bounded normal-route, controlled
fallback and concurrency cases, inspect health/latency/errors/OOM/restarts, and
restore the prior Compose state on any failure. Provider-call count and spend must
be explicitly bounded before that test. Passing the cap test would justify proposing
an OCI resize to 1/4 and a separate QAOS 1/8 VM; it would not itself authorize either.

Verification: Console returned to the live Monitoring page with no mutable action.
JSON parse and Git whitespace checks only; no product regression suite applicable.
