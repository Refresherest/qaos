# HANDOFF-101 — Opt-In Executive Factory

WO-117 complete on feat/operational-builder-chain, baseline 1c344c7.
Read OWNER-DECISION-023, WO-117 and VERIFICATION-103.

create_executive now supports explicit per-instance python_file_workspace
opt-in without changing defaults or global registries. Construction performs no
output writes. 213 tests, compile and 188 imports pass; active data unchanged.

Next proposed work: assess how an application can explicitly submit a validated
Task intent while preserving PlannerManager, ObjectiveManager and execution
lifecycle ownership. Do not bypass planning through persisted-record edits or
expand capability types, shell/Git authority or provider scope. No submission
API is authorized by the completed factory work. Stop here.
