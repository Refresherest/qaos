# OWNER-DECISION-034 — Separate Cloud Worker Target

2026-09-04. Authority: repository owner selected WO-151 Option A.
Select a separate cloud worker VM as the target, preserving the existing
QAOS-OmniRoute host and the project boundaries in OWNER-DECISION-033.

Authorize only the next read-only OCI tenancy capacity/usage/cost assessment.
Establish whether a separate worker's compute and boot/storage allocation fits
actual available entitlements. Do not infer free capacity from the existing VM's
idle RAM or from public marketing limits. Read-only access or redacted Console
evidence may be used; never request API secrets or private-key contents.

No provisioning, quota-change request, billing upgrade, spending, installation,
instance resizing, migration, restart or workload execution authorized. Do not
shrink OmniRoute to free quota. If capacity is unavailable or chargeable, stop
for an explicit budget/host decision. Shared-host workers are not the fallback.
WO-151's proposed controls and resource targets remain design, not proven readiness
or approval of an exact OCI shape/image. Obtain a concrete resource/setup decision
after assessment and before any external changes.
