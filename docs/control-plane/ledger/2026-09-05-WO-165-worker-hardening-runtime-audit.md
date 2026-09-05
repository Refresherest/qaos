# WO-165 — QAOS Worker Hardening and Runtime Audit

2026-09-05; baseline `209152a`; `feat/operational-builder-chain`.
Authority: owner instructed "proceed" from WO-164's explicit next action.
Objective: inspect the live worker network exposure and ARM64 runtime baseline,
then define the next safe decision without changing network rules or installing
software. Status: COMPLETE / decision required before mutation.

## Scope and non-goals

- Read the OCI VCN, subnet and associated security-list rules.
- Read the worker kernel, architecture-adjacent runtime and isolation baseline.
- Reconcile the findings with WO-151's separate-worker boundary.
- Do not change OCI networking, guest firewall, packages, daemons, users,
  credentials, OmniRoute, QAOS product code or active data.
- Do not run a candidate container or claim isolation/runtime validation.

## Live network findings

`qaos-worker` and `qaos-omniroute` share `qaos-vcn` (`10.0.0.0/16`) and the
regional public `qaos-public-subnet` (`10.0.0.0/24`). The subnet uses `Default
Security List for qaos-vcn`. Its observed rules are:

| Direction | Source / destination | Protocol | Rule |
| --- | --- | --- | --- |
| Ingress | `0.0.0.0/0` | TCP | destination port 22 |
| Ingress | `0.0.0.0/0` | ICMP | type 3, code 4 |
| Ingress | `10.0.0.0/16` | ICMP | type 3 |
| Egress | `0.0.0.0/0` | all | all traffic |

Therefore SSH is globally reachable at the OCI network layer and outbound
traffic is unrestricted. OCI also reported no network security group on the
worker. A network security group cannot narrow an allow rule inherited from the
subnet because applicable security-list and NSG rules are additive. Editing the
shared default list could affect OmniRoute, so no live rule was changed.

## Live guest findings

A strict-host-key SSH inventory of `qaos-worker` reported:

| Field | Observed value |
| --- | --- |
| Kernel | `6.17.0-1020-oracle` |
| Architecture | `aarch64` (verified by WO-164) |
| AppArmor service | active |
| Cgroups | cgroup v2 (`cgroup2fs`) |
| `/dev/kvm` | absent |
| Docker / containerd / runsc / runc / Podman | not found on `PATH` |
| Cloud-init | done |

No package index update, download or daemon change occurred. The temporary
helper-only SSH key copy used for inspection was deleted; the owner's original
key remained in its ignored location.

## Runtime compatibility and selection boundary

Docker's current Ubuntu documentation supports Ubuntu 24.04 and ARM64, while
warning that published container ports can bypass `ufw` and that Docker manages
iptables rules. gVisor's current installation documentation supports ARM64 on
Linux 5.6+ and prefers its signed Debian repository; installation can configure
Docker and Docker integration requires a daemon restart. The host meets only
these coarse prerequisites. Compatibility with the QAOS harness and enforcement
of no network, no host mounts, no Docker socket, resource/process/output limits
and cleanup remain unverified.

Official references:

- https://docs.docker.com/engine/install/ubuntu/
- https://gvisor.dev/docs/user_guide/install/
- https://gvisor.dev/docs/user_guide/quick_start/docker/
- https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/securitylists_working.htm

## Decision required

The preferred immediate containment is a guest firewall rule that permits SSH
only from an owner-approved administrative CIDR and denies other unsolicited
inbound traffic, followed by an SSH continuity test and automatic rollback if
the new rule blocks management. This is worker-specific and leaves OmniRoute's
shared OCI rule unchanged. The exact administrative CIDR is not established and
must not be guessed.

A stronger later boundary is a dedicated worker subnet/security list (or worker
VCN), but the current primary VNIC cannot be treated as migrated merely by adding
an NSG. That change needs a separate network migration/recreation plan.

After ingress is resolved, the recommended first runtime experiment is pinned
Docker Engine plus pinned gVisor `runsc`, one harmless ARM64 fixture, no published
ports, no network, no writable host or socket mounts, and WO-151's provisional
candidate caps. This is a proposal, not installation authority or runtime
designation.

## Stop condition

WO-165 is complete. Stop before changing the guest firewall or installing a
runtime. Owner input is required for the administrative source CIDR. Then create
a separate reversible firewall work order; runtime installation remains a later
work order after SSH continuity is proven.
