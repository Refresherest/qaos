# HANDOFF-094 — Objective Discovery

Baseline f04e975, feat/operational-builder-chain. Work order WO-103; authority
OWNER-DECISION-019.

`python -m qaos.main objectives --workspace <path>` now lists every Objective
in persisted order with safely quoted ID, status, and goal. Legacy IDs appear
as null, repeated goals remain separate, empty workspaces succeed explicitly,
and corrupt/duplicate data fails without partial output or repair.

Modified main.py; added commands/objectives.py, discovery tests, WO-103,
VERIFICATION-096 and this handoff; updated project-state records. 177 tests pass;
compile/import checks pass (186 modules); no-write behavior is verified.

Next bounded step: assess whether CLI objective execution should report its new
canonical ID, especially on failure. Do not change output compatibility without
an owner decision; UI, retry policy and migration remain excluded.
