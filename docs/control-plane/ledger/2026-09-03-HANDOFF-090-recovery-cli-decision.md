# HANDOFF-090 — Recovery CLI Decision

Baseline: 835664e, feat/operational-builder-chain. Work order: WO-099.

The owner selected Option A. OWNER-DECISION-018 governs an explicit-workspace,
exact-ID one-shot recovery CLI with 0/1/2 statuses. Documentation only changed.

Next: implement the approved command through main.py and a narrow adapter over
OperationalSession, with focused CLI/subprocess tests and a real failed-attempt
recovery rehearsal. Do not add ID discovery, UI, retry policy, or migrations.
