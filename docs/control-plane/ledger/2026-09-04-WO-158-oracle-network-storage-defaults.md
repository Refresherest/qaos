# WO-158 — Oracle Network and Storage Default Inspection

2026-09-04; baseline `5ebff02`; `feat/operational-builder-chain`.
Authority: owner "next" after WO-157. Objective: inspect the remaining Create
compute instance defaults without creating or changing resources. Scope: signed-in
Console reads and control-plane records only. Status: COMPLETE / launch remains
blocked pending explicit manifest selections and the A1 entitlement decision.

## Observed draft defaults

The signed-in Johannesburg Create compute instance wizard was advanced through its
Security, Networking and Storage sections without reaching or submitting Create.

| Area | Tenancy-visible default / state |
| --- | --- |
| Security | Shielded instance enabled for the default Micro-compatible draft |
| Primary network | `Select existing virtual cloud network` selected |
| VCN | No VCN selected; selector disabled until its prerequisite selection resolves |
| Subnet | `Select existing subnet` selected; subnet required and not selected |
| Private IPv4 | Automatic assignment selected but disabled until subnet selection |
| Public IPv4 | Automatic assignment disabled; warning requires a public subnet |
| IPv6 | Disabled; warning requires an IPv6-enabled subnet |
| SSH | `Generate a key pair for me` selected; Oracle warns the private key is shown once |
| Boot volume | Default 46.6 GB; custom size/performance off |
| Encryption | In-transit encryption on; customer-managed key off |
| Additional block volume | None; attach action disabled in the incomplete draft |

These are UI defaults, not approved QAOS manifest values. In particular, generating
an Oracle key pair would conflict with the prior requirement for a separately
authorized dedicated identity and durable public-key reference. No key was generated
or downloaded.

## Manifest consequences

The draft cannot establish a network plan without choosing or creating a VCN and
subnet. WO-151 proposed a separate worker network, so reusing OmniRoute's network
must not be inferred from the existing-network default. A future approved manifest
must name exact VCN/subnet CIDRs, route and security rules, public-IP policy, operator
source `/32`, SSH public-key reference, and teardown behavior. Network creation is a
state-changing operation and remains unauthorized.

The 46.6 GB default plus the existing 47 GB OmniRoute boot volume totals about
93.6 GB, below the documented 200 GB Always Free aggregate, but this arithmetic is
not a billing guarantee. The EUR 1.85 estimate and Oracle source conflict recorded
in WO-157 remain unresolved cost evidence.

The draft was exited by direct navigation to the Instances page. It was not
submitted; no Create action, key generation/download, VCN/subnet creation, volume
attachment, or account change occurred. OmniRoute remained untouched.

## Stop condition

Read-only defaults are resolved. Exact image OCID, rootfs artifact/digest, dedicated
SSH identity, network manifest, cost/teardown guard, and owner route decision remain
launch blockers. The next architectural step is an owner selection among the three
routes in WO-157; do not continue form preparation as though a route were approved.

Verification: Console accessibility/DOM inspection, direct return to the Instances
page, JSON parse and Git whitespace checks only. No runtime suite is applicable.
