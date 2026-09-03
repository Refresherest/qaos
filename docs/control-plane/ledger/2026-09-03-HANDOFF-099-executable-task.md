# HANDOFF-099 — First Executable Task

WO-111 implements OWNER-DECISION-021 on feat/operational-builder-chain,
baseline f461906. Read WO-109, OWNER-DECISION-021, WO-111 and VERIFICATION-101.

QAOS now has one opt-in Task-owned deterministic executable intent. It creates
one confined Python file, directly verifies exact output, persists bounded
evidence, preserves lifecycle truth and refuses overwrite on recovery. The
default runtime and description-only tasks remain unchanged.

All 191 tests pass; compile and 188-module import sweep pass; active data is
unchanged. OpenHands SMOKE-002 remains separately blocked at the last recorded
Cloud parent-runtime startup state.

Stop condition reached. A future work order must assess the next smallest
builder increment from this evidence. Do not generalize the print-only fixture
or add model/shell/Git authority without an owner-approved contract.
