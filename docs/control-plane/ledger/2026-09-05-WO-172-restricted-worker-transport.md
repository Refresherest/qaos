# WO-172 — Restricted Worker Transport and Synthetic Exchange

2026-09-05; baseline `60035a4`; `feat/operational-builder-chain`.
Authority: after WO-171 completed, the repository owner replied "proceed" to the
separate restricted-transport authorization checkpoint required by
OWNER-DECISION-035.
Status: COMPLETE; restricted transport installed and synthetic-only live evidence
recorded on 2026-09-06.

## Pre-change gate (historical snapshot)

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

The local protocol checkpoint now implements canonical UTF-8 JSON and 8-byte
big-endian framing, exact schemas, UUID/nonce/time/runtime validation, canonical
member order, path/count/size/hash limits, exact reads and trailing-input refusal.
Its 42 focused tests pass. Independent review returned `ACCEPT WITH NOTES`; its sole
non-blocking malformed-Unicode exception note was corrected and regression-tested.

At this pre-change checkpoint, live identity, key, authorized-key and sudoers
changes had not begun. The next checkpoint at that time was the root-owned broker
lifecycle: replay markers, immutable staging, bounded refusal/response, fixed
`harmless` launcher invocation and exact cleanup, followed by local review before
installation.

That broker lifecycle checkpoint is now implemented locally. Replay claims use
exclusive creation plus file and directory fsync; request staging is private,
no-follow, exclusive and self-cleaning; correlated policy/runtime/cleanup failures
produce bounded hashed frames; cleanup failure dominates; and only the pinned
`harmless` fixture can be invoked. The combined local protocol/broker suite reports
53 passed and one intentional Windows skip for real Linux `flock` contention.
Independent review returned `ACCEPT WITH NOTES` with no remaining blocker or major
finding. Its remaining notes are the real Linux lock, no-follow, directory-fsync,
ownership/mode, forced-key, sudoers and installed-hash checks required during the
rollback-protected live checkpoint.

That local checkpoint authorized generation of the dedicated key and the
rollback-protected live installation recorded below. Generated candidates and QAOS
source remained prohibited throughout.

## Completion evidence

A dedicated ED25519 transport key was generated under the ignored external
`_Oracle_Keys/Qaos-Worker/Transport Key` directory. Its private half was neither
printed nor transferred. The initial Windows invocation accidentally applied the
literal passphrase `""`; this was detected without disclosure and removed before
the first successful authenticated exchange. The public identity did not change.

Before worker mutation, a transient 15-minute rollback timer was armed. The live
installation created locked system identity `qaos-broker`, a root-owned forced-key
entry using OpenSSH `restrict`, and one exact sudoers grant for
`/usr/local/sbin/qaos-worker-broker`. Broker and protocol installed hashes matched
their local reviewed files:

- broker: `d0432efc08309eaa41e9e09e741c43da22582dcf6ab43e18796fbfe6588c157d`
- protocol: `5b1357f3e79c4ea6e3519c7e265b2ba8c7301750ef0530f7f538bd5b86b5c79c`

One direct synthetic exchange completed. A separate bounded suite proved a second
synthetic success, replay rejection and silent pre-correlation rejection of an
unexpected field, unsafe member path and bad content hash. The tightened negative
oracle was rerun after review, bringing the total to eleven workload-bearing
routing calls, within the owner's cap of twelve. No
generated candidate or QAOS source was transferred.

Installed Python files compiled, sudoers validation passed, the owned staging tree
and `qaos-negative-*` container search were empty, and a fresh strict-host-key
administrator login succeeded. Only then was the rollback timer stopped and its
temporary helper removed. Focused tests report 71 passed and one intentional
Windows-only `flock` skip; the full suite reports 533 passed and one skip.

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
