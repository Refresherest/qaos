# HANDOFF-130 — Oracle Worker Design Gate

C:/Projects/qaos; feat/operational-builder-chain; WO-150 baseline 0d1890a.
Read AGENTS.md, authority policy, CURRENT_STATE.md, OWNER-DECISION-032,
WO-150, VERIFICATION-120 and VERIFICATION-119's proposed contract/control tests.

Oracle SSH inventory succeeded with owner-verified pinned ED25519 identity.
Ubuntu ARM64, 2 CPUs, about 12 GiB RAM, 39 GiB disk free; Docker running and
OmniRoute healthy. No ready untrusted worker verified. Preserve OmniRoute and
its secrets; no provisioning, runtime installation, daemon reload or tests ran.
Local laptop VM preparation is no longer the selected next direction.

Next proposed WORK_PACKAGE: cloud worker isolation DESIGN only. Compare separate
worker VM against an enhanced isolated interim worker, resolve resource limits,
safe transfer, compatibility, setup/restart impact and rollback. Do not assume a
second free VM or authorize co-resident arbitrary execution. Request approval for
the concrete plan before downloads, configuration, spend or smoke execution.

Connection reference/fingerprint is in VERIFICATION-120; use the existing external
key without copying or exposing contents. A temporary public known-host file was
removed, so reconnect requires verified pinning. Stop if server identity differs.
Keep credentials out of repository records. Preserve unrelated dirty/untracked work.
