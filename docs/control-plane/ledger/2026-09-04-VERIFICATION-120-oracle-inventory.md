# VERIFICATION-120 — Oracle Cloud Inventory

2026-09-04; baseline 0d1890a. Read-only inventory complete, not sandbox acceptance.
Owner-supplied endpoint 84.12.71.92, SSH user ubuntu. ED25519 SHA256 fingerprint
2gEWVJRayr5MFkBbvXqNeNUxAIRUQqQ449Gy7u6Zebw matched handshake and scanned public key.
Strict checking stayed enabled using a task-specific public known-host file.
Private key was used by SSH from its existing external folder, not read/displayed,
copied or staged. The task-specific public host-key file was removed after use.
Reconnect must reestablish a matching pinned host entry; never accept a changed key.

Windows ssh-keyscan failed with unsupported sntrup key-exchange method. Existing
Git-bundled ssh-keyscan retrieved the public key; ssh-keygen independently matched
the supplied fingerprint. Initial sandbox authentication could not read the key;
approved unsandboxed SSH succeeded without key permission changes. No packages
were installed to obtain access. Remote host auditing may record these logins.

## Live observations

| Resource | Observed |
| --- | --- |
| OS / architecture | Ubuntu 24.04.4 LTS; Linux aarch64; kernel 6.17.0-1018-oracle. |
| CPU | 2 online logical CPUs. No OCI shape/billing inference from this alone. |
| RAM | 11,927 MiB total; 1,498 MiB used; 10,428 MiB available at initial snapshot. |
| Swap | None. |
| Root disk | 45 GiB displayed; 6.0 GiB used; 39 GiB available. |
| Docker | Running; server 29.1.3; cgroup v2, systemd driver. |
| Security capabilities | Docker reports AppArmor, built-in seccomp and cgroup namespaces; AppArmor service active. Not per-worker enforcement proof. |
| OmniRoute | Only running container listed; healthy, up 8 days; image diegosouzapw/omniroute:latest. |
| Port binding | 127.0.0.1:20128 -> 20128/tcp. Public ingress was not assessed. |
| Workload snapshot | OmniRoute 0.00% CPU, 835.9 MiB memory, 21 PIDs. Snapshot, not peak-load evidence. |
| Existing limits | memory=0, nanoCPUs=0, pids unset; restart unless-stopped. No explicit limits shown; unchanged. |
| Images | OmniRoute 2.64 GB and hello-world 22.6 kB. No image pulled or run. |
| Isolation alternatives | /dev/kvm absent; runsc, kata-runtime, podman not found on PATH. Runtime listing reports runc entries. No hardware-backed nested VM or enhanced worker runtime proven. |

Commands executed remotely, with bounded output and no container environment dump:

```sh
uname -sm
uname -r
cat /etc/os-release
getconf _NPROCESSORS_ONLN
free -m
df -h /
systemctl is-active docker
command -v docker podman
systemctl is-active apparmor
stat -fc %T /sys/fs/cgroup
test -e /dev/kvm && ls -l /dev/kvm
command -v runsc kata-runtime podman
docker version --format '{{.Server.Version}}'
docker info --format '{{json .SecurityOptions}} {{.CgroupVersion}} {{.CgroupDriver}}'
docker ps --format '{{.Names}} | {{.Image}} | {{.Status}} | {{.Ports}}'
docker stats --no-stream --format '{{.Name}} | {{.CPUPerc}} | {{.MemUsage}} | {{.PIDs}}'
docker image ls --format '{{.Repository}}:{{.Tag}} | {{.Size}}'
docker info --format '{{json .Runtimes}}'
docker inspect --format '{{.Name}} restart={{.HostConfig.RestartPolicy.Name}} memory={{.HostConfig.Memory}} nanoCPUs={{.HostConfig.NanoCpus}} pids={{.HostConfig.PidsLimit}}' omniroute
docker ps --filter name=omniroute --format '{{.Names}} {{.Status}}'
```

Last health check still reported healthy. Runtimes feature output was verbose and
truncated; do not treat it as a comprehensive runtime audit. No OCI account/API,
instance metadata endpoint, credential environment, provider database or Compose
secret file was inspected. Free-tier entitlements, VM resizing and another-instance
availability remain unverified; owner describes this as the existing free VM.

## Recommendation and boundaries

Cloud-first supersedes local VM setup. Capacity is promising for a small sequential
worker experiment, but neither sufficient isolation nor peak-load headroom is proven.
Do not run arbitrary candidates under ordinary Docker beside OmniRoute yet.
Docker documents that capabilities/mounts and kernel vulnerabilities can limit
isolation: [Docker security](https://docs.docker.com/engine/security/).

Prefer separating credential-bearing coordination from eventual untrusted workers.
A separate disposable worker VM is the stronger operational separation to evaluate,
but tenancy capacity/cost cannot be assumed. If the existing VM must host an interim
worker, require a separately reviewed enhanced isolation design and accept that
co-resident workloads still share host failure/resource risks. No zero-interference
promise. Do not alter OmniRoute limits or restart Docker opportunistically.

gVisor is a candidate to evaluate, not selected/installed: its documentation lists
ARM64 and Linux 5.6+ support, compatible with the observed architecture/version at
that basic level. Its non-KVM platform may avoid requiring /dev/kvm, but ARM64
platform/runtime behavior and workload compatibility must be established in a later
gate. Package installation may configure Docker, so no generic install command is
approved on this live service host. [Installation](https://gvisor.dev/docs/user_guide/install/),
[platform guide](https://gvisor.dev/docs/architecture_guide/platforms/).

Proposed initial design target, NOT a reservation: one worker at a time, at most
1 CPU and 1 GiB RAM initially, 256 MiB disposable scratch, bounded image/disk budget,
short time/output/process limits. Measure actual runtime overhead first; reduce or
refuse jobs if host headroom/OmniRoute health is inadequate. The 2-CPU host remains
small. No GPU needed for this validation gate; later project capacity is separate.

Retain VERIFICATION-119's candidate/test/evidence ownership and independent control
tests, replacing local Hyper-V assumptions with a cloud-specific runtime proposal.
Require denied candidate network, no host/secret/Docker-socket mounts, immutable
inputs, strict result parsing, cleanup and no automatic promotion. No laptop or
direct-host fallback. Durable source/evidence must survive worker disposal.

Next recommended work: design-only comparison of separate-worker-VM versus an
enhanced isolated interim worker, with exact budgets, installation/restart impact,
transport and rollback plan; obtain owner approval before any setup or smoke.
No new provider/model readiness or free-tier guarantee is established here.

Verification: observed read-only commands and record JSON/whitespace checks only;
no product changes or regression rerun. Unrelated dirty skills/untracked files and
active data preserved. Existing services left running. No security scan claimed.
