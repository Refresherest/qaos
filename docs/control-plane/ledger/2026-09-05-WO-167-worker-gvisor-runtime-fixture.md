# WO-167 — QAOS Worker gVisor Runtime Fixture

2026-09-05; baseline `bab9659`; `feat/operational-builder-chain`.
Authority: the owner replied "Ok, next" after WO-166 identified a pinned ARM64
Docker plus gVisor runtime experiment as the next separately authorized work.
Objective: install a pinned experimental runtime on `qaos-worker` and execute one
harmless, digest-pinned, no-network fixture under the provisional WO-151 limits.
Status: COMPLETE / installation, runtime, fixture, containment and cleanup checks
passed on 2026-09-05; generated-code admission remains prohibited.

## Scope and non-goals

- Use the official Docker Ubuntu repository and official gVisor release repository.
- Resolve and hold exact ARM64 package versions before running a fixture.
- Register gVisor as an explicit Docker runtime without making it Docker's default.
- Run one reviewed BusyBox fixture with no network or published ports, read-only
  root, bounded scratch, unprivileged identity, no capabilities, no privilege
  escalation, and WO-151's CPU, memory, process and deadline settings.
- Verify the runtime from the host, collect bounded evidence, and remove the test
  containers.
- Do not transfer QAOS source, clone the repository, expose a job endpoint, add a
  Docker-group user, mount host/project/key/socket paths, run generated code,
  change QAOS product contracts, contact OmniRoute, or claim production readiness.

## Installed and pinned runtime

The signed repositories exposed these candidates, which were installed and held:

| Component | Installed package version | Installed executable SHA-256 |
| --- | --- | --- |
| Docker Engine / CLI | `5:29.8.0-1~ubuntu.24.04~noble` | `dockerd`: `3a699717ec78f96bcb144853543db9465bffc347e5930fc20a95b9ec1b6b65a7` |
| containerd | `2.3.4-2~ubuntu.24.04~noble` | `c84656b0cd90245b6257b56ba8c3e9632871daf4b8168e7e4d19f6990b604278` |
| gVisor runsc | `20260831.0` (`release-20260831.0`) | `d5679775682cd4cb11ba7bf7bd8e04235622aa8797d518dd280064e5cd27ed5d` |

Docker's repository signing key SHA-256 was
`1500c1f56fa9e26b9b8f42452a553675796ade0807cdce11975eb98170b3a570`;
the dearmored gVisor repository key SHA-256 was
`6980344d5d10b0fe4dea6b0a8a3f12a50ff1b2f3f81c40fed43dd942eace0184`.
APT signature verification is the package-integrity boundary; locally recorded
executable hashes provide repeatable installed-artifact evidence, not independent
publisher attestation.

APT also installed Docker's recommended buildx, Compose and rootless-extras
packages plus their dependencies. No rootless service was configured, no user was
added to the Docker group, and no build or Compose operation was performed. Their
removal is not required by this fixture and was not broadened into this work order.

The gVisor package was configured before Docker finished installing, so the initial
Docker runtime inventory did not include `runsc`. The official `runsc install`
registration step updated `/etc/docker/daemon.json`; after a Docker restart the
runtime inventory included `runsc`. The daemon configuration SHA-256 was
`36604e23d4f122c291f0c10be02bf76ecdec3ae3c10205d37edf45f8953fb1ff`.

Official references:

- https://docs.docker.com/engine/install/ubuntu/
- https://gvisor.dev/docs/user_guide/install/
- https://gvisor.dev/docs/user_guide/quick_start/docker/
- https://gvisor.dev/docs/user_guide/compatibility/linux/arm64/

## Harmless fixture manifest

The multi-architecture image resolved to ARM64/Linux and was executed by immutable
digest:

```text
busybox@sha256:fc6dddc4c44b1bfe37f41cae8e67d1693828e8f42a91862816d7953e2c9d3f23
```

Applied Docker controls:

| Boundary | Applied value |
| --- | --- |
| Runtime | explicit `runsc` |
| Network | `none`; no published ports |
| Root filesystem | read-only |
| Scratch | `/tmp` tmpfs, 256 MiB, `noexec,nosuid,nodev` |
| CPU | 1 CPU (`1000000000` NanoCPUs) |
| Memory | 1 GiB; memory-plus-swap also 1 GiB |
| Processes | PIDs limit 32 |
| Identity | UID/GID `65534:65534` |
| Privilege | all capabilities dropped; `no-new-privileges` |
| Outer deadline | 30 seconds, then TERM and five-second kill allowance |

The fixed command verified the unprivileged UID, successful scratch write, denied
root-filesystem write and failed outbound HTTP attempt, then emitted exactly
`QAOS_RUNTIME_FIXTURE_OK`. Docker reported `exited/0/false`, proving clean exit and
no OOM for this fixture. The test container was removed.

A second short-lived observation container allowed host-side inspection. The host
showed a `runsc-gofer` and `runsc-sandbox`/`gvisor_sentry`, including one CPU and
1-GiB memory runtime arguments. It was then removed. No experiment containers or
published ports remained. Host available memory was 7,357 MiB after the fixture.

## Security and continuity checks

- Docker and containerd active: PASS.
- `runsc` registered but not selected as Docker's default: PASS.
- Worker-specific SSH `/32` rule survived install and daemon restart: PASS.
- Fresh SSH after Docker restart: PASS.
- Docker socket `root:docker 0660`; `ubuntu` is not in Docker group: PASS.
- Host/project/key/socket mounts supplied to fixture: none.
- Test containers remaining: zero.
- Published ports remaining: zero.
- OmniRoute and shared OCI security list: intentionally untouched.
- Temporary helper-only SSH key copies: deleted.

## Evidence boundary and remaining gates

This validates that the pinned ARM64 Docker/gVisor combination can start and clean
up the harmless constrained fixture on this worker. Configuration inspection proves
the requested limits were passed to Docker/gVisor. It does not yet prove hostile
over-limit enforcement, descendant cleanup, output truncation, metadata denial by
packet observation, tamper resistance, durable job/result framing, or safe execution
of generated code. A failed HTTP request alone is not independent packet evidence.

Docker/gVisor installation is therefore VERIFIED for this fixture, not VALIDATED
for the future QAOS workload and not DESIGNATED as a QAOS execution service.

## Removal path

If this experiment is abandoned, remove only its held packages and repository
configuration after confirming there are no owned containers/images to retain:
unhold and purge `runsc`, Docker Engine/CLI, containerd and Docker's installed
plugins/extras; remove `/var/lib/docker`, `/var/lib/containerd`, the two repository
list/key files and `/etc/docker/daemon.json` only under a separately authorized
cleanup work order. Recheck SSH persistence afterwards. Do not touch the instance,
boot volume, VCN, subnet, shared security list, OmniRoute or owner key files.

## Stop condition

WO-167 is complete. Stop before staging QAOS inputs or running generated code. The
next separate work order should implement and review a fixed trusted launcher plus
synthetic negative fixtures for input, filesystem, network/metadata, memory, PIDs,
scratch, output, deadline, descendant cleanup and result-integrity gates. No real
credentials or uncontrolled exhaustion tests are permitted.
