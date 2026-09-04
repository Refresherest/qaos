# WO-156 — Micro Launch Manifest Preparation

2026-09-04; baseline 2b08140; feat/operational-builder-chain.
Authority: owner Proceed on WO-155 read-only manifest preparation.
Objective: resolve public artifact identities and account-dependent launch gates.
Scope: public metadata reads and control-plane records. No binaries executed,
infrastructure created, credentials generated, account changes, product edits,
trial-credit consumption or OmniRoute operations. Preserve unrelated dirty work.
Acceptance: evidenced pins, explicit missing fields and no launch with unknowns.
Status: INCOMPLETE / waiting for account evidence and remaining artifact selection.

## Candidate manifest (NOT executable or approved)

| Field | Value / evidence state |
| --- | --- |
| Region / shape / count | af-johannesburg-1 / VM.Standard.E2.1.Micro / 1; prior owner Console quota evidence, recheck at launch |
| Image candidate | Canonical-Ubuntu-24.04-Minimal-2026.07.17-0; official release July 21, 2026 |
| Regional image OCID | ocid1.image.oc1.af-johannesburg-1.aaaaaaaai4aj5re2mrkjf5446nyou7nnrr67ms2ftohe7nanjoh5x7e22dua |
| Image launch compatibility | UNVERIFIED in tenancy: Micro compatibility, x86-64, eligibility, minimum disk and availability |
| Boot storage | Proposed 50 GB, VPU10, no autotuning/backups/replicas; account cost preview UNVERIFIED |
| Runtime candidate | gVisor release-20260817.0, gvisor-x86_64.tar.bz2; systrap/direct runsc proposed by WO-155 |
| Runtime verification | Published SHA512 retrieved; archive bytes NOT downloaded, hashed, installed or validated |
| Python filesystem bundle | UNRESOLVED; require immutable x86-64 stdlib-capable artifact, provenance and digest before execution |
| Network | Separate new VCN/subnet/IGW and restrictive rules proposed; exact CIDRs, aggregate rule manifest and cost UNRESOLVED |
| Administrative ingress | Operator-approved public source /32 UNRESOLVED; SSH only, no public application ingress |
| SSH identity | New dedicated public-key reference UNRESOLVED; no reuse of OmniRoute key, no private-key contents in records |
| Deployment approval | NONE; no create/install/run authorization |

Image source: [Oracle image catalog](https://docs.oracle.com/en-us/iaas/images/ubuntu-2404/canonical-ubuntu-24-04-minimal-2026-07-17-0.htm).
This is an identified candidate, not a claim it is the newest or security-reviewed
image. Record supported kernel and reviewed patch procedure before setup; any
change of image invalidates the candidate pin and requires manifest revision.

Runtime artifact:
https://github.com/google/gvisor/releases/download/release-20260817.0/gvisor-x86_64.tar.bz2

Published SHA512:
`bd8271a7742f90e53373b2a8613f37f3ae2c765ff5e2e611a75a47167a323cab7519b149c50273307743491713525a14ad1b3e398651c93b16f3e248dfeff3dd`

[Official release](https://github.com/google/gvisor/releases/tag/release-20260817.0),
[published checksum file](https://github.com/google/gvisor/releases/download/release-20260817.0/SHA512SUMS).
Future setup must compare downloaded archive bytes to this digest before extraction
and retain complete sidecar layout. Publisher checksum is not independent security
validation or proof of resource-fit. No moving latest reference in launch manifest.

## Retrieval evidence

PowerShell Invoke-RestMethod in sandbox failed with 'Authentication failed, see
inner exception.' Approved external read reached the proposed release-bucket
gvisor.tar.zstd.sha512 but returned NoSuchKey. Did not disable TLS or install tools.
Read official GitHub release API instead: assets include x86_64/aarch64 bz2 archives
and SHA256SUMS/SHA512SUMS. Retrieved small SHA512SUMS successfully. No archive
download or remote worker access. This resolves checksum-location failure, not
runtime admission. All queries were public; no API token or account secret used.

## Next evidence and stop

Request only the next necessary Console evidence: inspect the Create instance
form's image/shape selection for Micro and Ubuntu 24.04 Minimal x86-64, without
clicking Create or creating network/key resources. Supply image name/build,
compatibility/Always Free label and boot-size/cost preview when shown. If the
candidate is unavailable, report available supported builds, do not substitute
automatically. Console preview alone cannot establish all future usage costs.

After that, resolve rootfs artifact and exact network/admin fields read-only;
cost uncertainty or missing identity continues to block launch. Do not request a
private key or API secret. New key generation is a later explicitly authorized
step. No arbitrary-code execution until reviewed launcher/fixtures and WO-155
controls are implemented and independently tested in later approved work.

Verification: JSON and Git whitespace checks; metadata inspection only, no runtime
suite or independent reviewer claim. Architecture-awareness preserved the distinction
between publisher evidence, tenancy eligibility, deployment approval and validation.
Unrelated skills/untracked work untouched. Stop pending inputs; rollback is record
revision only. WO-156 remains open, not falsely marked complete.
