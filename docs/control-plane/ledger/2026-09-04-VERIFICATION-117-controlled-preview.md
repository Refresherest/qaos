# VERIFICATION-117 — WO-145

2026-09-04; baseline 1738e6c; Python 3.14.3; Windows.
Outcome: ACCEPT WITH NOTES; same-agent checklist, not independent review.

Added planner/controlled_brief.py pure interpret(directory, brief), reusing existing
PythonProjectIntentV2. Added commands/preview_project.py for strict two-option
parsing and JSON preview/error output; main.py adds help/dispatch only. The grammar
validates full ASCII input before case/space normalization; no partial matching,
default selection, free-form reasoning or new intent/schema/registry.

Verification using .venv/Scripts/python.exe:

- `-m pytest tests/test_controlled_preview.py -q -p no:cacheprovider --basetemp
  C:/Projects/qaos/.wo145-focused-tmp`: 96 passed in 8.57s.
- `-m pytest -q -p no:cacheprovider --basetemp C:/Projects/qaos/.wo145-full-tmp`:
  450 passed in 171.43s; active-data hashes and timestamps unchanged across run.
- `-m compileall -q src tests`: passed.
- pkgutil.walk_packages/importlib.import_module sweep: 198 modules imported.
- `tools/architecture_inspect.py`: 200 files, same 22 existing findings; outside scope.
- `-B -m qaos.main preview-project --directory Example --brief "Count LINES and words"`:
  exit 0, exact preview envelope with canonical metrics [words,lines].
- Git comparison: build_project.py and planner/intents.py unchanged.

Coverage: all 15 metric orderings under normal/uppercase/space variants and exact
intent round trips, all seven canonical selections; empty/wrong-type/overlong
briefs and exact 256/257 boundary; malformed connectors, duplicates, synonyms,
negation, appended instructions, punctuation, controls and Unicode lookalikes;
existing invalid directory cases; option/refusal/JSON/exit/payload redaction.

Side-effect guard test forbids store/session creation, build/root delegation,
process launch, socket construction and os.system during preview. Fresh -B CLI
success/refusal leaves disposable state/output empty and unchanged, creates no
objective and preserves active data. Separate CLI build without permission still
fails; explicitly enabled build persists the same intent as preview. Collision
still refuses and preserves output. No automatic preview-to-build link exists.
These checks plus source inspection establish the bounded implementation path,
not an untrusted-code sandbox or a universal guarantee about future changes.

Architecture-awareness kept planner interpretation pure and CLI a consumer of the
existing intent. No session/store/network/execution imports in the new modules.
Unexpected failures report exception type only; invalid inputs use static diagnostics
with empty stdout. Existing API permissions, v1/v2 builder and tests unchanged.
No providers, credentials, OpenHands retest, migration or Content OS scope changes.

Files: two new source modules, new test file, main.py, three ledger records and two
current-state files. Unrelated dirty skills and untracked configuration/drafts/
tools/test directories preserved; WO-145 focused/full artifacts left untracked.
Record JSON/whitespace checks run before checkpoint. Stop before next walkthrough.
