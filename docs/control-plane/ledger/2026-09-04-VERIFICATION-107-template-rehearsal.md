# VERIFICATION-107 — WO-125

2026-09-04; baseline 591ea3b. Outcome: ACCEPT WITH NOTES.

`.venv/Scripts/python.exe docs/control-plane/ledger/wo125_template_probe.py`
passed. Six fresh processes: build, import/use, CLI discovery, collision build,
file-only recovery and default-session recovery. Exit codes 0, 0, 0, 1, 1, 1.
The 1 codes are probe-defined expected refusals, not a new product CLI contract.

Generated text_stats_v1 returned fixed expected ASCII/multiline and Unicode
counts and rejected None. Import/use emitted no output; bytecode generation was
disabled by the probe. Import and discovery preserved workspace hashes/timestamps.
Collision raised FileExistsError. Both disabled recovery modes returned exactly
`template is not enabled`, without state/output file writes. Objective, Plan Task,
QueueItem and queue action remained failed. Successful records and output were
preserved. Temporary workspace removed; active-data hashes/timestamps unchanged
across the probe.

Additional commands:

- `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider --basetemp C:/Projects/qaos/.wo125-full-tmp`: 245 passed.
- `.venv/Scripts/python.exe -m py_compile docs/control-plane/ledger/wo125_template_probe.py`: passed.
- `.venv/Scripts/python.exe tools/architecture_inspect.py`: 192 source files;
  existing duplicate/registry/singleton findings remain out of scope.

Same-agent Reviewer checklist, not independent review. Architecture-awareness
kept the work confined to a ledger probe using existing public APIs and WO-121
helpers. No product source, provider configuration, credentials or unrelated
files changed. No new blocker discovered. This proves the reviewed deterministic
template only, not arbitrary app generation, hostile-process isolation or
OpenHands readiness. Import sweeps were not rerun for this probe-only change.
