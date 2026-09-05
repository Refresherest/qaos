# WO-168 — QAOS Worker Trusted Launcher and Negative Tests

2026-09-05; baseline `26cc20d`; `feat/operational-builder-chain`.
Authority: the owner replied "proceed" after WO-167 identified a fixed trusted
launcher and bounded synthetic negative-test bundle as the next work order.
Objective: implement and verify a root-operated, allowlist-only worker launcher
for fixed synthetic fixtures without accepting QAOS source or generated code.
Status: COMPLETE / implementation and bounded live verification passed on
2026-09-05; same-agent verification only.

## Scope and non-goals

- Keep the launcher in `tools/qaos-worker`, outside `src/qaos`, because it is
  infrastructure validation tooling rather than a product execution contract.
- Accept only fixed fixture identifiers. Do not accept caller-supplied commands,
  images, paths, mounts, Docker flags, environment variables or source archives.
- Enforce one fixture at a time, fixed immutable image/runtime settings, bounded
  output retention, a 30-second deadline and exact container cleanup.
- Exercise reviewed synthetic input/admission, filesystem, network/metadata,
  memory, PIDs, scratch, output, deadline, descendant and result-integrity cases.
- Do not run generated code, stage the QAOS repository, call OmniRoute, use real
  secrets, publish ports, weaken SSH, create a remote service/API or change QAOS
  product source, tests, registries, persistence or active data.

## Implemented launcher boundary

Created `tools/qaos-worker/qaos_worker_launcher.py` and installed an identical
root-owned copy at `/usr/local/sbin/qaos-worker-launcher` on `qaos-worker`.
The final installed file SHA-256 is:

```text
0bc39f9ab6eb917b0983ee3fab9dae79cf7c97f0103d654b30f33ad6fb89828e
```

The launcher is `root:root 0755`, must run with effective UID 0, uses a
non-blocking root lock at `/run/qaos-worker-launcher.lock`, generates its own
container name under the exact `qaos-negative-` prefix and removes that exact
container in a `finally` boundary. It calls Docker with argument arrays rather
than a candidate-controlled shell.

Every fixture uses:

- immutable ARM64/Linux image
  `python@sha256:b64631e04e4920160c50fbe8d8df828f7f35f06f425cb44aa09bca53e708a35a`;
- explicit `runsc`, `--network=none`, no published ports and no mounts;
- read-only root plus 256-MiB `noexec,nosuid,nodev` `/tmp`;
- 1 CPU, 1-GiB memory with no additional swap and 32-PID limit;
- UID/GID `65534:65534`, all capabilities dropped and no-new-privileges;
- Docker logging disabled, launcher-owned per-stream capture capped at 1 MiB;
- 30-second monotonic deadline, container kill, five-second process grace and
  mandatory exact-container removal.

The launcher returns one compact launcher-owned JSON record containing the fixed
fixture/image identity, stable specification hash, independently observed Docker
exit/OOM state, termination reason, bounded byte counts, hashes and previews.
Candidate output is retained as untrusted evidence and cannot replace these fields.

## Synthetic canary and fixture results

A zero-content synthetic host canary exists at
`/opt/qaos-worker/host-canary`, owned `root:root 0600`. It contains no credential
or owner data and was never mounted. The filesystem fixture verified that this
host path was absent inside the sandbox, root writes failed and bounded scratch
writes succeeded.

| Gate | Bounded fixture and result |
| --- | --- |
| Harmless calibration | Exact `QAOS_HARMLESS_OK`; exit 0; no OOM. |
| Admission/input | `../escape` rejected by the argparse allowlist with exit 2 before container creation; non-root invocation rejected with exit 2. |
| Filesystem/identity | Synthetic host canary absent, root write denied, `/tmp` write succeeded; exact expected output and exit 0. |
| Network/metadata | Both public destination and `169.254.169.254:80` connection attempts failed under network-none; exact expected output and exit 0. |
| Memory | A fixed 1.1-GiB allocation under the 1-GiB cap exited 137 with Docker `OOMKilled=true`; host remained responsive. |
| PIDs | Attempt to create 40 child processes hit the 32-PID boundary, then terminated/reaped created children; exact expected output and exit 0. |
| Scratch | Attempt to write 257 MiB into 256-MiB tmpfs raised an OS error; exact expected output and exit 0. |
| Output | Candidate emitted 1 MiB plus one byte; launcher retained exactly 1,048,576 bytes, marked `stdout_limit` and removed the container. |
| Deadline | Fixed 35-second sleep was killed at 30 seconds; exit 137; container removed. |
| Descendants | Parent plus 60-second child was killed at deadline; afterward zero containers, `runsc-gofer`, `gvisor_sentry` or `sleep` processes remained. |
| Result integrity | Candidate printed `{"status":"PASS"}` but exited 7; launcher recorded candidate failure rather than accepting the text. |
| Concurrency | While one deadline fixture held the lock, a second fixture was rejected with exit 1; primary remained bounded and cleaned up. |

After every phase, the exact experiment-container count was zero. Published-port
count was zero. Host available memory after the OOM fixture was 6,899 MiB. The
source-specific SSH rule remained present, and all temporary launcher transfer,
test-output and helper-key files were deleted.

## Verification performed

- Local and worker `python3 -m py_compile`: PASS.
- Exact-output self-review improvement applied and low-impact fixtures rerun:
  PASS.
- All ten allowlisted fixture cases: PASS against their trusted expected result.
- Unknown input, non-root and concurrent admission tests: PASS.
- Deadline and descendant host-process cleanup checks: PASS.
- JSON parse and whitespace/diff checks: PASS.
- Architectural inspection: no new QAOS domain, registry, API, persistence or
  provider coupling; infrastructure remains a consumer/supporting boundary.
- Review independence: not claimed; implementation and verification were
  performed by the same agent.

## Evidence boundary

This proves the installed launcher enforces the tested fixed-fixture boundary on
the current pinned host/runtime/image combination. It does not prove arbitrary
language/package compatibility, packet capture outside the sandbox, resistance
to every kernel/runtime vulnerability, reboot recovery, durable remote job
transport, archive/path validation, authenticated result collection, main-QAOS
integration or safety of model-generated code.

The runtime/launcher are VERIFIED for these fixtures. They are not yet VALIDATED
for a QAOS generated-code workload and are not DESIGNATED as a QAOS execution
service.

## Rollback

The worker copy can be removed by deleting only
`/usr/local/sbin/qaos-worker-launcher`, its Python cache, the lock file and the
synthetic `/opt/qaos-worker/host-canary` under a separately authorized cleanup
work order. The repository file remains reviewable evidence unless reverted by
the owner. Docker/gVisor package removal remains WO-167's broader removal path.

## Stop condition

WO-168 is complete. Stop before accepting files or generated code. The next
separate work should receive independent review of this launcher and negative-test
evidence, then propose a bounded immutable input-manifest and authenticated result
transport contract. No SSH-exposed arbitrary-command service is an acceptable
shortcut.
