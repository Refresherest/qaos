# WO-162 — OmniRoute 1-OCPU/4-GB Container Cap Test

2026-09-04; baseline `602d287`; `feat/operational-builder-chain`.
Authority: owner explicitly authorized a reversible 1-CPU/4-GB cap test and no
more than 12 OmniRoute routing calls. Objective: test whether the existing
OmniRoute gateway remains healthy and responsive at the proposed allocation.
Status: COMPLETE / 1-OCPU/4-GB container cap test passed and original limits
restored.

## Scope and safety contract

- Keep the OCI VM itself at its existing 2-OCPU/12-GB shape.
- Temporarily apply a live Docker cap of 1 CPU and 4 GB to the existing
  `omniroute` container.
- Preserve the original container limits, observed as unlimited CPU and memory.
- Run no more than 12 small routing calls and record the exact count.
- Observe health, latency, routing errors, restart count, OOM state and resource
  use before, during and after the calls.
- Restore the original unlimited container limits after the test regardless of
  outcome, and roll back immediately on a health, restart, OOM or request failure.
- Do not resize or create OCI resources, change networking or routing policy,
  expose credentials, or modify QAOS product code.

## Preflight evidence

- SSH host ED25519 fingerprint matched the previously recorded pin:
  `SHA256:2gEWVJRayr5MFkBbvXqNeNUxAIRUQqQ449Gy7u6Zebw`.
- Container state: running and healthy; restart count 0; OOMKilled false.
- Original limits: NanoCPUs 0 and memory 0 (unlimited).
- Immediate preflight sample: 16.31% CPU, 844.4 MiB of 11.65 GiB, 21 PIDs.

## Results

The first `docker update --cpus 1 --memory 4g` attempt was rejected before any
change because Docker required the memory-swap setting to be updated at the same
time. Inspection confirmed all three original limit values remained zero. The
successful command applied 1 NanoCPU, 4 GiB memory and 4 GiB memory-swap, meaning
no swap allowance beyond the memory cap.

Immediately after applying the cap, the container remained running and healthy
with restart count 0 and OOMKilled false. It used 845 MiB of 4 GiB (20.63%),
0.00% sampled CPU and 21 PIDs.

Nine of the authorized maximum 12 routing calls were made:

| Test | Calls | Result | Observed latency |
| --- | ---: | --- | --- |
| Sequential: one each to `qaos-csa`, `qaos-pe`, `qaos-reviewer` | 3 | All HTTP 200 | 143 ms, 435 ms and 3,820 ms |
| Concurrent: two simultaneous calls per route | 6 | All HTTP 200 | 239–343 ms |

Each request used the existing authenticated OpenAI-compatible chat-completions
route, requested an exact short reply and imposed an eight-token output ceiling.
Response bodies and credentials were not recorded. No controlled fallback call
was attempted because no already-established non-mutating mechanism existed to
force a primary-route failure; changing live route policy would exceed this work
order. The unused three-call allowance was not consumed.

After all nine calls, the capped container was still running and healthy with
restart count 0, OOMKilled false, 859.3 MiB of 4 GiB (20.98%), 0.03% sampled CPU
and 21 PIDs.

## Rollback and final verification

`docker update` and the Docker update API both retained zero-valued limit fields
instead of clearing the active caps. These attempts did not disrupt the healthy
container. The container was then recreated from the unchanged existing
`/opt/omniroute/compose.yml` service definition, which restored NanoCPUs, memory
and memory-swap to their original zero values. After the normal health-check
startup period, final state was running and healthy, restart count 0, OOMKilled
false, about 1,010 MiB used, 21 PIDs, and an authenticated non-routing models-list
request passed. The temporary SSH tunnel was closed.

## Assessment and stop condition

The test passes for OmniRoute's observed role as an external-model routing
gateway: 1 OCPU and 4 GB handled all nine bounded sequential/concurrent calls
without request error, health degradation, restart, OOM or material memory
pressure. Together with WO-161's seven-day metrics, this supports assigning
OmniRoute 1 OCPU/4 GB and reserving the other 1 OCPU/8 GB of the documented A1
allowance for a separate QAOS worker.

This result does not validate retry storms, provider outages, controlled fallback,
large concurrent agent fleets or long-duration operation under a hard cap. No OCI
resize or QAOS instance creation was performed or authorized. Stop here pending a
separate owner decision on the infrastructure change.
