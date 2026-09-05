# WO-163 — OmniRoute A1 Resize to 1 OCPU / 4 GB

2026-09-04; baseline `731e3e6`; `feat/operational-builder-chain`.
Authority: owner instructed "proceed" after WO-162 passed and identified the
next separately authorized infrastructure phase. Objective: resize only the
existing `qaos-omniroute` A1 Flex VM from 2 OCPUs/12 GB to 1 OCPU/4 GB, then
verify service recovery and capacity release. Status: COMPLETE / resize and
service recovery passed on 2026-09-05.

## Scope and safety contract

- Preserve the existing instance, boot volume, VCN, IP assignments, image and
  OmniRoute configuration.
- Confirm the editor shows `VM.Standard.A1.Flex`, Always Free eligibility,
  1 OCPU and 4 GB before submission.
- Gracefully shut down the Ubuntu guest before the shape change, following
  Oracle's current resize guidance; restart after the change.
- Verify OCI running state, 1-OCPU/4-GB shape, pinned SSH identity, Docker and
  OmniRoute health after restart.
- If the target shape is rejected or service recovery fails, preserve evidence
  and restore 2 OCPUs/12 GB when the Console permits.
- Do not create the separate QAOS worker, alter networking, generate credentials,
  change billing/account state or modify QAOS product code in this work order.

## Pre-change evidence

- Signed-in Console: `qaos-omniroute` running in `af-johannesburg-1`, AD-1,
  `VM.Standard.A1.Flex`, 2 OCPUs, 12 GB, public IP `84.12.71.92`.
- Prepared edit draft: same A1 shape and image; Always Free-eligible; 1 OCPU,
  4 GB, 1 Gbps; Save changes enabled.
- WO-162 established healthy bounded routing at the target allocation and
  restored the original Docker state.

## Results

The pre-change SSH host key matched the pinned ED25519 fingerprint and OmniRoute
was running and healthy with restart count 0 and OOMKilled false. Ubuntu accepted
a graceful `systemctl poweroff`. The prepared Console edit was then submitted and
the expected instance-reboot confirmation accepted.

OCI progressed through Stopping and Starting to Running. The same instance OCID,
AD-1, fault domain, image, VCN and public IP remained visible. Final Console shape
configuration is:

| Field | Verified value |
| --- | --- |
| Shape | `VM.Standard.A1.Flex` |
| OCPU count | 1 |
| Memory | 4 GB |
| Network bandwidth | 1 Gbps |
| Public IP | `84.12.71.92` |

Post-resize SSH retained the same pinned host identity. The guest reported one
online CPU and 3,897 MiB total RAM: 1,589 MiB used and 2,308 MiB available, with
no swap. Root storage remained 45 GiB total, 6.0 GiB used and 39 GiB available.
Docker was active. OmniRoute was running and healthy with restart count 0,
OOMKilled false, no Docker CPU/memory limit, 1.163 GiB current use (30.56% of the
guest), 0.02% sampled CPU and 21 PIDs. An authenticated non-routing `/v1/models`
request passed and returned the existing catalog. No provider routing call was
made. The temporary SSH tunnel was closed.

The existing container Compose definition and all OCI network/storage settings
were left unchanged. No rollback was required. Oracle's current shape-change
documentation states that flexible-shape CPU/memory changes preserve IP and VNIC
attachments and reboot a running instance; the observed result matched that
behavior:
https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/resizinginstances.htm

## Stop condition

WO-163 is complete. OmniRoute now occupies 1 OCPU/4 GB and the proposed 1-OCPU/
8-GB A1 allocation is numerically available for a separate QAOS worker under the
conservative 2-OCPU/12-GB baseline. This does not create, designate or validate
that worker. Stop before launch: the separate worker still requires a completed
manifest, dedicated SSH identity, network/administrative-ingress decision, boot
volume cost guard and explicit final create authorization.
