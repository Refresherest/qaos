# HANDOFF-125 — Controlled Preview

C:/Projects/qaos; feat/operational-builder-chain; WO-145 baseline 1738e6c.
Read AGENTS.md, authority policy, CURRENT_STATE.md, OWNER-DECISION-030,
WO-145 and VERIFICATION-117. Same-agent review, not independent delegation.

    python -B -m qaos.main preview-project --directory Example --brief "count words and lines"

Output is one JSON object with status=preview, grammar_version=1 and existing
v2 intent. It is not a completed or approved build. Grammar accepts only count
plus one to three distinct metrics joined by and, with ASCII case/space variants.
No partial matching, synonyms, arbitrary text, models or execution. Bad requests
exit 2 with static diagnostic/empty stdout; unexpected errors exit 1, type only.
Interpreter API: qaos.planner.controlled_brief.interpret(directory, brief).

Building remains a separate explicitly authorized build-project request; there
is no preview file loader, permission transfer, persistent approval or automatic
execution. Build CLI and all existing API permissions remain unchanged.

Next proposed WORK_PACKAGE: bounded operator preview/refusal walkthrough with
disposable no-write checks and a separately authorized build; document supported
phrases and limitations without adding grammar or permission. Stop after current
implementation checkpoint; do not broaden to free-form interpretation.

Preserve three unrelated dirty skills and untracked configuration/drafts/tools/
test directories. WO-145 test artifacts remain untracked. No provider/credential,
OpenHands or active-data migration changes. Git log identifies this checkpoint.
