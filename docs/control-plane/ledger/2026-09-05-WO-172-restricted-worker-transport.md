# WO-172 — Restricted Worker Transport and Synthetic Exchange

2026-09-05; baseline `60035a4`; `feat/operational-builder-chain`.
Authority: after WO-171 completed, the repository owner replied "proceed" to the
separate restricted-transport authorization checkpoint required by
OWNER-DECISION-035.
Status: IN PROGRESS; authorization and pre-change baseline recorded. No worker
mutation or transport key creation has occurred.

## Pre-change gate

A fresh strict-host-key administrative connection verified `qaos-worker`, UID 1001
for the administrative session, launcher SHA-256
`0bc39f9ab6eb917b0983ee3fab9dae79cf7c97f0103d654b30f33ad6fb89828e`, and
launcher ownership/mode `root:root 0755`. Effective SSH settings reported public-key
authentication enabled, password authentication disabled and root login restricted
to keys. No `qaos-negative-*` container residue was reported.

Windows rejected the owner's original private key after quarantine removal because
its ACL had become too broad. The original was not modified. A disposable helper
copy received a narrow ACL, completed the audit and was verified deleted after a
targeted permission correction. No private-key contents were read or printed.

The next checkpoint is local broker/controller implementation and protocol tests.
Live identity, key, authorized-key and sudoers changes must wait until that exact
code passes local security review.

## Objective and architecture

Implement and independently verify Option A's authenticated, one-request/
one-response length-framed transport on the existing `qaos-worker` SSH listener.
Use a new dedicated controller key and locked worker identity with a root-owned
forced broker. Exercise only synthetic bytes and the already reviewed fixed
`harmless` launcher fixture. This is infrastructure transport evidence, not a new
QAOS registry or product source of truth.

## Authorized changes

- Add a reviewable broker and controller probe under `tools/qaos-worker` plus local
  protocol tests.
- Generate one ED25519 transport key under the Git-ignored
  `_Oracle_Keys/Qaos-Worker` tree; never print or copy private-key contents.
- On `qaos-worker`, create one locked non-administrative OS identity whose
  root-owned authorized-key entry forces only the broker and applies OpenSSH
  `restrict`.
- Install the broker root-owned and grant that identity one exact passwordless
  sudo command for the broker only; no general shell, Docker, launcher, file or
  administrative sudo.
- Validate strict framing/schema/path/size/hash/time/replay/runtime pins, root-owned
  staging, bounded response, and exact cleanup.
- Run successful and negative synthetic exchanges over a fresh strict-host-key SSH
  connection. Invoke only the existing fixed `harmless` launcher fixture.
- Schedule a recoverable rollback before SSH/user/sudoers mutation; cancel it only
  after administrative and restricted-key continuity checks pass.

## Non-goals

- No generated code, QAOS source, real acceptance bundle, model output or secret is
  transferred or executed.
- No arbitrary command, caller-selected fixture/image/runtime/environment/mount,
  archive, SFTP, shell, port forwarding or new network listener.
- No product Artifact/Queue integration, automatic retry, model validation or
  designation.
- Do not change OmniRoute, OCI network rules, the administrative SSH identity, or
  the existing launcher/runtime policy except for the broker's exact invocation.

## Verification and stop condition

Verify local protocol tests, compile/import/whitespace checks, installed hashes and
permissions, exact authorized-key restrictions and sudoers syntax. Prove one bounded
success and replay/schema/path/hash failures, zero owned staging/container residue,
and fresh administrative SSH continuity. Obtain independent review. Record rollback
steps and exact evidence, then STOP for a new owner decision before any generated
candidate or QAOS-source transfer.
