# WO-164 — QAOS A1 Worker Launch

2026-09-05; baseline `9bbb756`; `feat/operational-builder-chain`.
Authority: owner approved the separate QAOS worker allocation, authorized a
dedicated SSH identity, supplied its local storage location, and authorized the
final Create action by replying "Ok, next" after the final manifest was shown.
Objective: launch and minimally verify one separate QAOS worker without
installing or designating a runtime. Status: COMPLETE / launch and SSH capacity
verification passed on 2026-09-05.

## Scope and non-goals

- Launch one `qaos-worker` in South Africa Central (Johannesburg), AD-1.
- Use `VM.Standard.A1.Flex` with 1 OCPU and 8 GB memory, preserving the owner's
  conservative 2-OCPU/12-GB split with the existing 1-OCPU/4-GB OmniRoute VM.
- Use a dedicated ED25519 SSH identity stored outside source control under the
  ignored `/_Oracle_Keys/` tree; transmit only the public key to OCI.
- Verify the OCI work request, Running state, image, shape and a minimal SSH
  guest-capacity probe.
- Do not install Docker, OpenHands, QAOS packages or other software; do not
  expose application ports, change network rules or claim runtime validation.

## Final manifest and observed OCI state

| Field | Verified value |
| --- | --- |
| Instance | `qaos-worker` |
| Region / placement | `af-johannesburg-1`, AD-1, FD-1 |
| State | Running; Create work request Succeeded at 100% |
| Shape | `VM.Standard.A1.Flex`, 1 OCPU, 8 GB, 1 Gbps |
| Image | `Canonical-Ubuntu-24.04-Minimal-aarch64-2026.08.25-0` |
| VCN / subnet | `qaos-vcn` / `qaos-public-subnet` |
| Addressing | public IPv4 `92.4.147.163`; private IPv4 assigned by OCI |
| Boot storage | default 46.6-GB encrypted boot volume; no added block volume |
| Instance OCID | `ocid1.instance.oc1.af-johannesburg-1.anvg4ljr2pc3dvacppkzcblkk6qmdqrj7qu6ug4x65w3kawy4se2mpcs7ioq` |

The cost preview showed EUR 1.85/month for the boot volume and explicitly said
the estimate does not reflect tier unit pricing. It is therefore retained as a
gross-price warning, not evidence of either a charge or a zero-cost outcome.

The final OCI review reported Secure Boot, Measured Boot and Trusted Platform
Module disabled. It also reported no network security group and a public IPv4
address. These facts must be treated as hardening work, not silently described
as a shielded or private worker.

## SSH identity and guest verification

The dedicated key pair is stored under
`_Oracle_Keys/Qaos-Worker/{Private Key,Public Key}` and the entire
`/_Oracle_Keys/` directory is Git-ignored. No private-key contents were printed
or committed. The OCI review displayed the matching ED25519 public-key comment
`qaos-worker-2026-09-05`.

The first SSH attempt reached the host but Windows OpenSSH rejected the original
key file because both the owner account and the owner's `qaasi` account had
access. A temporary helper-only copy was created solely for the verification
probe and deleted immediately afterwards; the owner's original remained in its
requested directory.

Strict host-key checking then authenticated to `ubuntu@92.4.147.163`. The guest
reported:

- 1 online CPU;
- 7,915 MiB total memory, 376 MiB used and 7,538 MiB available;
- no swap;
- `aarch64` architecture; and
- 45 GB root filesystem, 1.3 GB used and 43 GB available.

This proves launch, SSH identity matching and baseline guest capacity. It does
not validate QAOS or OpenHands on the worker.

## Stop condition

WO-164 is complete. Stop before runtime installation or further cloud changes.
The next separately authorized work should audit/restrict SSH ingress on the
public subnet, establish the worker runtime manifest for ARM64, and define a
rollback/removal condition before installing anything.
