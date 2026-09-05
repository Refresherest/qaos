# WO-166 — QAOS Worker SSH Ingress Restriction

2026-09-05; baseline `a325054`; `feat/operational-builder-chain`.
Authority: the owner asked Codex to obtain the stable public IPv4 address, then
replied "ok, next" after Codex identified the reversible SSH firewall checkpoint
as the next action.
Objective: restrict `qaos-worker` guest SSH ingress to the verified owner
connection address without changing the shared OCI network rule or installing
runtime software. Status: COMPLETE / live, continuity and persistence checks
passed on 2026-09-05.

## Scope and non-goals

- Establish the administrative source address using two independent live
  observations.
- Replace only the guest firewall's broad TCP/22 exception with that address as
  a `/32` rule.
- Schedule an automatic rollback before mutation, verify a new SSH connection,
  persist the successful rule, and cancel the rollback.
- Do not change the shared OCI security list, subnet, VCN, OmniRoute, IPv6
  policy, outbound policy, packages, daemons other than the transient rollback
  unit, credentials, QAOS product code or active data.
- Do not install or designate Docker, gVisor or an untrusted execution runtime.

## Administrative source evidence

The browser connection's public IPv4 endpoint returned `102.33.120.222`. The
worker's SSH service log independently recorded `102.33.120.222` as the source
of the successful public-key login. The exact administrative CIDR used for this
work order is therefore `102.33.120.222/32`.

This evidence proves the address used during the work order. It does not create
a guarantee that the owner's internet provider will never change that address.
If it changes, Console access is required to restore or replace the rule.

## Existing guest boundary

The Ubuntu image already had an iptables-nft INPUT chain with established-flow,
ICMP and loopback allowances, a broad new-connection TCP/22 allowance, and a
final reject. `netfilter-persistent` was enabled and `/etc/iptables/rules.v4`
was present. UFW was not installed. The work therefore reused the existing
iptables persistence boundary instead of adding another firewall manager.

## Change and rollback

Before changing the rule, a transient systemd timer was scheduled to restore
the broad TCP/22 allowance and save it after three minutes. The live rule was
then replaced with:

```text
-A INPUT -s 102.33.120.222/32 -p tcp -m tcp --dport 22 -m state --state NEW -j ACCEPT
```

The established-flow rule preserved the active management session. A separate,
fresh strict-host-key SSH connection then succeeded from `102.33.120.222`.
Only after that success was the restricted ruleset saved with
`netfilter-persistent`; the rollback timer was stopped and verified inactive.

## Verification

- Fresh SSH session: PASS (`fresh-ssh-ok`).
- SSH source recorded by worker: PASS (`102.33.120.222`).
- Live INPUT chain includes the source-specific TCP/22 rule: PASS.
- Broad source-independent TCP/22 new-connection rule absent: PASS.
- `/etc/iptables/rules.v4` includes the source-specific rule: PASS.
- `netfilter-persistent` enabled: PASS.
- Rollback timer inactive only after fresh-session success: PASS.
- Temporary helper-only SSH key copy deleted: PASS.
- Shared OCI security list and OmniRoute: intentionally untouched.

## Stop condition

WO-166 is complete. Stop before runtime installation or any OCI network
migration. The next separately authorized work order may define and install the
pinned ARM64 Docker plus gVisor runtime experiment described by WO-165, including
checksum evidence, a harmless no-network fixture, resource/process/output caps,
cleanup and removal conditions.
