# HANDOFF-120 — Approved Builder CLI Implementation

C:/Projects/qaos; feat/operational-builder-chain; WO-140 baseline 7d25f87.
Read AGENTS.md, authority policy, CURRENT_STATE.md, WO-139,
OWNER-DECISION-029 and VERIFICATION-114. WO-140 records approval only.

Next WORK_PACKAGE: scope and implement the explicit build-project CLI under
OWNER-DECISION-029. Reuse PythonProjectIntentV2 and OperationalSession; inspect
main.py, commands/objective.py, commands/recover.py, planner/intents.py and the
existing project-root validation before editing. Apply all WO-139 acceptance
requirements. Do not infer broader API/root changes or project recovery permission.

Verify focused/full tests, compile/import checks and fresh-process CLI behavior
with disposable state/output, preserving active data and existing successful output.
Record results and stop after the bounded implementation checkpoint.
No models, providers, OpenHands retest, natural-language interpretation or arbitrary
code. Existing three dirty skill files and unrelated untracked configuration,
drafts, tools and test directories remain outside scope. This checkpoint contains
only three new ledger records and two current-state updates; JSON/whitespace checks
only, no new runtime claim. Git log identifies the WO-140 checkpoint commit.
