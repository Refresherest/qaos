# HANDOFF-131 — Separate Cloud Worker Choice

C:/Projects/qaos; feat/operational-builder-chain; WO-151 baseline f3626e6.
Read AGENTS.md, authority policy, CURRENT_STATE.md, OWNER-DECISION-033, WO-151,
VERIFICATION-120 and VERIFICATION-119 control-test proposals.

Design complete; no deployment. Main QAOS and supporting QAOS-OmniRoute remain
separate in authority, credentials, deployment and work-order scope. Recommended
target is a distinct worker VM, not execution inside the existing routing host.

Next: owner selection of A (separate worker target, read-only OCI quota/cost check
only) or B (explicit co-resident risk/setup design). Do not assume spare free quota,
resize OmniRoute or provision on selection. Need Console read-only capacity/usage
evidence before exact resource plan. No secrets, installations, runtime smoke or spend.

Five records in this checkpoint: owner separation decision, design WO, handoff
and two current-state updates. JSON/whitespace checks only. Preserve dirty skills
and unrelated untracked files. Stop for owner decision.
