# HANDOFF-121 — Explicit Builder CLI

C:/Projects/qaos; feat/operational-builder-chain; WO-141 baseline 5d13fc3.
Read AGENTS.md, authority policy, CURRENT_STATE.md, OWNER-DECISION-029,
WO-141 and VERIFICATION-115. The command is a thin typed-intent consumer.

Usage (replace placeholders with existing, separate absolute directories):

    python -m qaos.main build-project --workspace <state> --output-root <output> --directory Example --metrics words,lines --enable-project text_stats_project_v2

All five options required once, any order. No defaults or prose interpretation.
State/output may not overlap or traverse reparse points. Output remains local
Windows/fixed NTFS. Exit codes: 0 completed, 2 invalid request/permission,
1 root/runtime/build failure. Objective ID is printed before execution; successful
summary includes published directory and normalized metrics. Runtime logs remain.
Use objectives --workspace <state> for discovery. Existing recover has no project
permission; it is intentionally not a project-recovery command. Existing outputs
are never adopted/overwritten. This is not an untrusted-code sandbox.

Next proposed WORK_PACKAGE: bounded operator walkthrough of the shipped CLI using
disposable, explicit state/output directories, including discovery and failure
diagnostics; record a reproducible operator example, without feature expansion.
Stop after the current verified implementation checkpoint.

Same-agent review, not independent delegation. Preserve modified three QAOS
skills, unrelated untracked configuration/drafts/tools/prior test directories.
WO-141 focused/full test directories remain untracked. No provider, OpenHands,
active-data migration, v1/v2 implementation or existing tests changed.
