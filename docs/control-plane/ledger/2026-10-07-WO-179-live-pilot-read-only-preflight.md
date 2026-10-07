# WO-179 — Read-Only Live Pilot Go/No-Go Preflight

2026-10-07; baseline `cce42c1` on `feat/operational-builder-chain`.
Authority: the owner's “Proceed” after WO-178's local-only ACCEPT, interpreted
as the next bounded, read-only evidence checkpoint in WO-175 and
DECISION-REQUEST-023 option 3A. Status: COMPLETE — independently reviewed
read-only NO-GO (VERIFICATION-130); no live authorization.

## Objective and architectural context

Refresh the account, resource, network, worker, runtime, cleanup and cost
evidence needed to decide whether a separately authorized one-request
`python-single` pilot is even eligible. WO-176's bridge and WO-178's attempt
authority are local-only. Historical screenshots, cost previews and the local
test suite cannot establish present cloud state or entitlement.

The canonical candidate and acceptance Artifacts remain the payload source of
truth; the QueueItem remains the one-attempt authority. A read-only preflight
does not create a candidate, claim a QueueItem, install the bridge, designate a
model or convert a passing script into workload validation.

## In scope

- Read-only Oracle Console inspection of current account tier/trial status,
  home region, A1 allocations and shapes, all relevant boot/block volumes,
  billing/usage and cost alerts, and worker/OmniRoute placement and network
  association. Record redacted, dated values and direct Oracle documentation.
- Read-only worker inspection over the already pinned administrative SSH
  identity, **only if** the original host pin validates and key handling is
  authorized. Verify guest identity, CPU/memory, runtime pins, policy, image
  cache, deployed bridge state, SSH continuity, and owned cleanup residue.
- Compare local reviewed installer/launcher source hashes to their accepted
  pins. Identify unresolved candidate/acceptance, cost, rollback and
  cross-store lifecycle prerequisites. Reconcile control-plane state records.

## Explicit non-goals

No account upgrade, spending, resource creation/deletion/resize, VCN or guest
firewall change, software install/update, image pull, bridge enablement,
candidate transfer, generated-code execution, QueueItem claim, request send,
retry, active JSON-to-SQLite cutover, Task/Objective adjudication or model
governance transition. Do not reveal or source-control credential values.

## Requirements, verification and stop

1. Use account-specific live observations for entitlement, allocation and
   charges; label missing values **unverified**, never infer zero cost from an
   estimate or an empty historical usage chart. Oracle's current general
   Always Free guide states 1,500 A1 OCPU-hours and 9,000 GB-hours monthly,
   equivalent to 2 OCPUs/12 GB for an Always Free tenancy, and 200 GB of
   combined boot/block storage in the home region. The trial-end guide says
   excess A1 may be disabled and later deleted. These are public terms, not
   proof of this tenancy's current state.
2. Do not run worker commands unless strict host-key verification succeeds.
   Use only bounded, read-only inventory commands; no test container or
   synthetic exchange. If a temporary key copy is needed, require the owner's
   specific approval and remove it after the probe.
3. Compare expected and observed pins, account/worker/OmniRoute capacity,
   storage, network ingress and cleanup. A missing or contradictory critical
   observation yields **NO-GO / insufficient evidence**, not a guessed PASS.
4. Record exact commands, results, source dates, unresolved risks and a
   separate proposed live authorization manifest. Verify control-plane JSON
   parsing and scoped whitespace. Obtain independent review before calling
   the preflight complete. Then **STOP**: no live mutation or request without
   a new scoped owner approval.

Primary Oracle references checked 2026-10-07:

- <https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm>
- <https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm>
- <https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/budgetsoverview.htm>
- <https://docs.oracle.com/en-us/iaas/Content/Billing/Concepts/costusagereportsoverview.htm>

## Evidence so far

- The local reviewed pilot deployment script SHA-256 remains
  `37d75c567231bdbe2d0255200331345001f02704d79557897d670e81c23e37e8`;
  the local pilot launcher SHA-256 remains
  `1b8e20cbc63999244862544f5c9933fb14cf9701d22b455bb753d4ebf4a81403`.
  This does **not** verify installed worker bytes.
- Oracle's current Budget documentation calls budgets soft limits and says
  alerts are evaluated periodically, every 24 hours. Cost reports are
  generated daily. Neither is a hard, immediate spending stop; no account-
  specific cost or zero-charge conclusion follows from these public pages.
- Oracle's current Always Free guide also warns that idle A1 instances may
  be reclaimed when its CPU, network and memory conditions all hold over a
  seven-day period. The idle-worker observation here is not a prediction of
  reclamation or a reason to generate artificial load.
- After the owner signed in on 2026-10-07, the Console showed a Free Tier
  account whose Free Trial had ended, with South Africa Central (Johannesburg)
  selected. The root-compartment instance list showed only `qaos-worker` and
  `qaos-omniroute`, both Running as `VM.Standard.A1.Flex` in AD-1. Worker was
  1 OCPU/8 GB with public IPv4 `92.4.147.163`; OmniRoute was 1 OCPU/4 GB.
  This matches the prior intended 2-OCPU/12-GB split, but the tenancy's home
  region was not independently confirmed.
- The Compute regional `af-johannesburg-1` service-limit view, filtered for
  `a1` and root compartment, showed `standard-a1-core-regional-count`: limit
  2, usage 2, available 0; `standard-a1-memory-regional-count`: limit 12 GB,
  usage 12 GB, available 0. The instance-list banner still advertised 3,000
  OCPU-hours and 18,000 GB-hours monthly, whereas Oracle's current public
  Always Free guide states 1,500/9,000 and the Free Tier trial-end guide says
  no more than 2 OCPUs/12 GB across A1 instances. Treat the observed 2/12
  service limit and documented post-trial boundary as the conservative gate;
  do not infer an extra 2/12 from the inconsistent banner.
- The root-compartment boot-volume list showed exactly two volumes, each
  47 GB, carrying an Always Free label. Both were attached to the named
  instances; combined observed boot storage is 94 GB. The root-compartment
  standalone block-volume list showed no items. This is not an exhaustive
  cross-compartment or cross-region inventory.
- The Universal Credits subscription list showed its Infrastructure entry as
  **SUSPENDED**, with renewal date 2026-09-19 and listed commitment value
  €0.00. Its detail view retained the historical €250.00 total commitment
  value; the 2026-08-21 through 2026-10-07 usage view showed €0.00
  consumption and 5 SKUs in one region. Cost Analysis for 2026-10-01 through
  2026-10-07 showed cost-to-date 0 for Compute, Block Storage, VCN and
  Telemetry. The page warns that billing estimates may omit actual usage and
  usage data is typically delayed about 24 hours. This is evidence of the
  displayed estimate, **not** a zero-future-charge guarantee.
- The Budgets list showed no budget rows. The shared default security list
  for `qaos-vcn` still allows stateful TCP/22 ingress from `0.0.0.0/0` and all
  protocol egress to `0.0.0.0/0`, plus the two expected ICMP ingress rules.
  The worker's primary VNIC was attached to `qaos-public-subnet`; its
  private IPv4 was `10.0.0.20`. Guest firewall enforcement remains unverified.
- The Oracle session subsequently returned to a password sign-in screen.
  No login field was automated and no account setting or resource was changed.
- On a later read-only continuation on 2026-10-07, the Oracle session was
  active again. Governance & Administration > Tenancy Details showed the
  `emergestrategic` tenancy as Active and its **Home region: JNB**. This
  independently confirms the observed Johannesburg resources are in the
  home region. Region Management listed South Africa Central
  (`af-johannesburg-1`) as the only Subscribed region, on a single page of
  regions; the others were Not subscribed. The root compartment's Child
  Compartments list showed no items with its default Active/Deleting status
  filter. Thus the earlier root-compartment instance and volume lists cover
  the currently active compartment hierarchy in the subscribed region, but
  not resource types the respective lists do not support or delayed updates.
- The saved worker host-key pin exists, but the direct Windows OpenSSH probe
  refused the existing private key's broad ACL before authentication. The
  owner approved a temporary owner-only helper copy, but the command carrying
  that copy-and-cleanup operation was rejected before process creation by the
  execution environment. No helper copy was created, the original key was not
  changed, and no guest inventory was obtained. Do not work around this gate
  by weakening host-key checking or exposing key contents.
- The existing local SSH agent was checked without touching the private key:
  `ssh-add -l` returned "Error connecting to agent: No such file or
  directory" and `Get-Service ssh-agent` showed Stopped/Disabled. Thus no
  already-loaded identity is available for a keyless read-only worker probe.
  No service was started and no authentication attempt followed.
- The owner then supplied `_Oracle_Keys/Qaos-Worker` on 2026-10-07. A
  filename, public-fingerprint and ACL-only inspection found the intended
  administrative private key in `Private Key/qaos-worker-ed25519`, with the
  matching public key fingerprint `SHA256:9VAdaALmDb+uc976j9tX8BXkcaagNSVNmvPH+mn5zWo`.
  Its ACL still grants `CodexSandboxOnline` Modify in addition to the owner,
  Administrators and SYSTEM, so the earlier Windows OpenSSH rejection has not
  been remediated. The separate `Transport Key/qaos-worker-transport-ed25519`
  has fingerprint `SHA256:J5TUQjE8yn5fDGwowNLfUeD4pBnyROYI2/OILu7qhIY`;
  WO-172 records that this identity is forced to the restricted broker, not an
  administrative inventory shell. The saved host pin fingerprint is
  `SHA256:GqlPbIsqbZHPSDNHaXUeiq2Vs7uuzPfS11KKtKFgkJY`. No private-key
  contents were read, copied or disclosed, no ACL was changed, and no SSH
  authentication attempt was made with either identity in this continuation.
- The owner placed an administrative-key copy at
  `C:/Users/qaasi/.ssh/Private Key/qaos-worker-ed25519`. Its inherited ACL
  grants only the owner, Administrators and SYSTEM; `ssh-keygen -lf` reported
  the expected `SHA256:9VAdaALmDb+uc976j9tX8BXkcaagNSVNmvPH+mn5zWo`.
  A fresh `ubuntu@92.4.147.163` login succeeded with `IdentitiesOnly=yes`,
  `StrictHostKeyChecking=yes`, `BatchMode=yes`, the saved dedicated
  `known_hosts`, and an eight-second connection timeout. The host identified
  as `qaos-worker`, `aarch64`. No private-key contents were displayed.
- Read-only worker inventory on 2026-10-07 found one CPU, 7,915 MiB total
  memory (7,354 MiB available at observation), no swap, and 41 GB free on
  the 45-GB root filesystem. Docker and containerd were active. Docker
  29.8.0, containerd 2.3.4 and runsc `release-20260831.0` matched WO-167;
  Docker used systemd/cgroup v2, listed `runsc`, and retained `runc` as the
  default. SHA-256 for `dockerd`, `containerd`, `runsc` and `daemon.json`
  matched all four WO-167 pins. The cached Python image digest matched
  `b64631e04e4920160c50fbe8d8df828f7f35f06f425cb44aa09bca53e708a35a`
  and inspected as ARM64. The BusyBox calibration image was also cached.
- The installed synthetic launcher, broker and exchange SHA-256 values
  matched WO-168/WO-172's respective `0bc39f9a...`, `d0432efc...` and
  `5b1357f3...` pins. The launcher and broker were root-owned mode 0755;
  exchange was root-owned mode 0644. The pilot launcher and
  `/etc/qaos-worker/enable-python-single-v1` were absent, confirming that
  WO-176's local bridge has not been installed or enabled on this worker.
  The restricted broker account, root-owned authorized-key entry and exact
  sudoers grant remained present; the authorized key's fingerprint matched
  the dedicated transport public key, `restrict` and `command=` each appeared
  once, and `visudo -cf` parsed the sudoers file. No restricted-key exchange
  was attempted, so its current end-to-end path remains untested.
- The live iptables INPUT chain and persisted `/etc/iptables/rules.v4` both
  retained the source-specific TCP/22 rule for `102.33.120.222/32`, with no
  broad new-SSH rule in INPUT; `netfilter-persistent` was enabled. UFW is not
  installed. This guest boundary is narrower than the shared OCI security
  list's `0.0.0.0/0` port-22 allowance. Fresh strict-key SSH succeeded both
  before and during inventory; it does not guarantee access if the owner's
  source address changes.
- `docker ps -a` showed no containers. The fixed broker staging directory
  had zero entries, and the `/tmp` `qaos*` search found none. Pilot staging
  and upgrade directories were absent; no `qaos-worker*` systemd unit was
  loaded. The existing zero-byte synthetic host canary remained in place.
  These checks found no owned pilot residue; they are not a broad cleanup of
  unrelated host state. No container was started, image pulled or worker
  file changed.
- A further read-only Console check at approximately 20:24 UTC on
  2026-10-07 showed `qaos-omniroute` Running with 1 A1 OCPU and 4 GB; its
  primary VNIC had private IPv4 `10.0.0.153` and was attached to
  `qaos-public-subnet` in `qaos-vcn`. The worker's Networking page showed
  private IPv4 `10.0.0.20` and its primary VNIC attached to the **same**
  subnet OCID. The subnet's Security tab listed exactly one associated
  security list, `Default Security List for qaos-vcn`. Its Security rules tab
  still showed stateful TCP/22 ingress from `0.0.0.0/0`, two ICMP ingress
  rules and all-protocol egress to `0.0.0.0/0`. This confirms that the broad
  OCI rule is shared by the two instances. The narrower worker guest rule
  does not establish an equivalent OmniRoute guest rule; no OmniRoute guest
  firewall inspection was performed. No networking setting was changed.
- A fresh strict-host-key administrative SSH check at approximately 20:24
  UTC returned exit code 0. `/etc/os-release` reported Ubuntu 24.04.4 LTS;
  `uname -r` reported `6.17.0-1020-oracle`. A separate exit-code-0 inventory
  reported `ubuntu`, hostname `qaos-worker`, `aarch64`, 1 CPU, 7,915 MiB
  memory total (7,357 MiB available at observation), 0 swap and 41 GB
  available on the 45-GB root filesystem. Docker/containerd were active;
  the version output was Docker 29.8.0, containerd 2.3.4 and runsc
  `release-20260831.0`. These are read-only point-in-time observations,
  not a workload, restricted-key exchange or pilot installation.
- A read-only local payload inventory found `data/artifacts.json` equal to
  `[]` (zero current canonical Artifacts), one non-pilot row in the active
  JSON queue and no isolated pilot SQLite queue file. The candidate and
  acceptance IDs used in local test fixtures are synthetic; their
  `assert True` acceptance script does not invoke the candidate. The
  reviewed local pilot launcher would run an acceptance script with the candidate path
  as an argument, but that alone does not prove the script invokes or checks
  it. No real candidate/independently authored acceptance pair or one-attempt
  QueueItem identity can be pinned from this workspace. This does not rule
  out artifacts in an external workspace that has not been supplied.

Additional read-only evidence provenance (2026-10-07): the Console paths
inspected were each instance's Networking tab and `qaos-public-subnet`'s
Security tab, followed by the associated security list's Security rules tab.
The administrative SSH calls used the exact pinned prefix below; the two
remote payloads and redacted, non-secret result excerpts were:

```text
cat /etc/os-release; uname -r
exit 0: PRETTY_NAME="Ubuntu 24.04.4 LTS"; VERSION_ID="24.04"; 6.17.0-1020-oracle
id -un; hostname; uname -m; nproc; free -m; df -h /; systemctl is-active docker containerd; docker --version; containerd --version; runsc --version
exit 0: ubuntu; qaos-worker; aarch64; 1 CPU; Mem 7915 total / 7357 available MiB; Swap 0; /dev/sda1 45G / 41G available; active / active; Docker 29.8.0; containerd 2.3.4; runsc release-20260831.0
```

Earlier Console and worker observations above are summarized with the
commands that produced them, but a full preserved per-command stdout and
exit-status transcript is not available. Independent review should treat
that provenance limit as a note or require a fresh bounded recheck; it must
not turn an historical summary into present-tense certainty.

Observed installed SHA-256 values (all match their historical fixed pins):

| Worker file | SHA-256 |
| --- | --- |
| `/usr/bin/dockerd` | `3a699717ec78f96bcb144853543db9465bffc347e5930fc20a95b9ec1b6b65a7` |
| `/usr/bin/containerd` | `c84656b0cd90245b6257b56ba8c3e9632871daf4b8168e7e4d19f6990b604278` |
| `/usr/bin/runsc` | `d5679775682cd4cb11ba7bf7bd8e04235622aa8797d518dd280064e5cd27ed5d` |
| `/etc/docker/daemon.json` | `36604e23d4f122c291f0c10be02bf76ecdec3ae3c10205d37edf45f8953fb1ff` |
| `/usr/local/sbin/qaos-worker-launcher` | `0bc39f9ab6eb917b0983ee3fab9dae79cf7c97f0103d654b30f33ad6fb89828e` |
| `/usr/local/sbin/qaos-worker-broker` | `d0432efc08309eaa41e9e09e741c43da22582dcf6ab43e18796fbfe6588c157d` |
| `/usr/local/sbin/qaos_worker_exchange.py` | `5b1357f3e79c4ea6e3519c7e265b2ba8c7301750ef0530f7f538bd5b86b5c79c` |

The authenticated checks used the same exact SSH prefix throughout:

```text
ssh -i 'C:\Users\qaasi\.ssh\Private Key\qaos-worker-ed25519' -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile='C:\Projects\qaos\_Oracle_Keys\Qaos-Worker\known_hosts' -o BatchMode=yes -o ConnectTimeout=8 ubuntu@92.4.147.163
```

The remote payloads were the following read-only commands; related commands
were grouped into single SSH sessions. All privileged inventory used
`sudo -n`:

```text
id -un; hostname; uname -m
nproc; free -m; df -h /; systemctl is-active docker containerd; docker --version; containerd --version; runsc --version
sudo -n sha256sum /usr/bin/dockerd /usr/bin/containerd /usr/bin/runsc /etc/docker/daemon.json /usr/local/sbin/qaos-worker-launcher /usr/local/sbin/qaos-worker-broker /usr/local/sbin/qaos_worker_exchange.py
sudo -n stat -c %n:%U:%G:%a:%s /usr/local/sbin/qaos-worker-launcher /usr/local/sbin/qaos-worker-broker /usr/local/sbin/qaos_worker_exchange.py /usr/local/sbin/qaos-worker-pilot-launcher /etc/qaos-worker/enable-python-single-v1; sudo -n docker info | grep -A6 Runtimes:
sudo -n docker image ls --digests --no-trunc; sudo -n docker ps -a; sudo -n ufw status numbered
sudo -n iptables -S INPUT; sudo -n grep -- --dport /etc/iptables/rules.v4; systemctl is-enabled netfilter-persistent
sudo -n docker info | grep -E "Cgroup|Architecture|Operating System|Runtimes|Default Runtime"; sudo -n docker image inspect python@sha256:b64631e04e4920160c50fbe8d8df828f7f35f06f425cb44aa09bca53e708a35a --format={{.Architecture}}; stat -fc %T /sys/fs/cgroup
sudo -n find /run/qaos-worker-broker/staging -mindepth 1 -maxdepth 1 -printf %f\\n; sudo -n find /tmp -maxdepth 1 -name qaos\* -printf %f\\n; sudo -n ls -ld /run/qaos-worker-broker/staging /var/lib/qaos-worker-pilot-stage /var/lib/qaos-worker-pilot-upgrade /opt/qaos-worker/host-canary; systemctl list-units --all --no-pager qaos-worker\*
getent passwd qaos-broker; sudo -n stat -c %n:%U:%G:%a:%s /var/lib/qaos-broker/.ssh/authorized_keys /etc/sudoers.d/qaos-worker-broker; sudo -n grep -c restrict /var/lib/qaos-broker/.ssh/authorized_keys; sudo -n grep -c /usr/local/sbin/qaos-worker-broker /etc/sudoers.d/qaos-worker-broker
sudo -n stat -c %n:%U:%G:%a:%s /var/lib/qaos-broker /var/lib/qaos-broker/.ssh; sudo -n grep -c command= /var/lib/qaos-broker/.ssh/authorized_keys; sudo -n visudo -cf /etc/sudoers.d/qaos-worker-broker
sudo -n ssh-keygen -lf /var/lib/qaos-broker/.ssh/authorized_keys
sudo -n cat /etc/sudoers.d/qaos-worker-broker; sudo -n grep -o /usr/bin/sudo /var/lib/qaos-broker/.ssh/authorized_keys; sudo -n grep -o /usr/local/sbin/qaos-worker-broker /var/lib/qaos-broker/.ssh/authorized_keys
```

None ran a workload or changed worker state.
- At the start of this checkpoint, `PROJECT_STATE.json` still described
  DECISION-REQUEST-024 as open and omitted completed WO-178. It has now been
  reconciled with CURRENT_STATE and VERIFICATION-129. This bookkeeping update
  does not confer live authority or prove account/worker readiness.

## Separate live-approval manifest still required

Before any live gate, identify the exact canonical candidate and independently
authored acceptance Artifact IDs, digests and origin; review the acceptance
script's actual invocation/assertions; pin the proposed staged installer and
worker runtime/image bytes; name the QueueItem and one-attempt request identity;
set a numeric cost ceiling and rollback owner; and specify account/worker/SSH,
cleanup and `UNKNOWN` stop criteria. WO-175 and DECISION-REQUEST-023 require a
separate owner approval for that exact manifest. None is supplied here.

Current result: **NO-GO / incomplete authorization and cost/acceptance gates**.
The observed 2/12 allocation fits the conservative published post-trial A1
boundary; JNB is the only subscribed home region and no active/deleting child
compartments were shown. The authenticated worker inventory now confirms the
historical runtime/image/synthetic-transport pins, guest SSH restriction and
empty owned staging/container state. The worker and OmniRoute share a public
subnet whose OCI list allows SSH from anywhere; OmniRoute's guest-side rule is
unverified. The local artifact store has no real pilot payload pair or pilot
attempt identity. The inventory does **not** exercise restricted-key transport
or validate generated code. Delayed billing evidence, numeric cost ceiling,
exact candidate and independently authored acceptance artifacts, rollback
owner, live installation manifest and separate scoped live approval remain
outstanding. The independent Reviewer accepted this bounded NO-GO preflight
with provenance notes in VERIFICATION-130. No pilot request was sent.
