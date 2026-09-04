# VERIFICATION-109 — WO-129

2026-09-04; baseline 8f977e4. Outcome: ACCEPT WITH NOTES.

`.venv/Scripts/python.exe docs/control-plane/ledger/wo129_cli_probe.py`: passed.
Eight top-level fresh processes: build, valid standalone use, invalid standalone
use, discovery, collision build, default recovery, file-only recovery and
old-template recovery. Exit codes: 0, 0, 2, 0, 1, 1, 1, 1. The 2 is the generated
app's invalid-argument contract; 1 codes are probe-defined caught refusals.
Build also runs its existing 16 internal verification children (not included in
the top-level count), confirming 15 CLI cases in persisted evidence.

Standalone execution uses Python -I from the output directory, without QAOS on
its import path. Counts and error streams match expected values. Discovery and
all disabled recovery calls preserve file hashes/timestamps. Same-target build
raises FileExistsError; Objective/Plan Task/QueueItem/action remain failed.
Successful records and source are preserved. Disposable workspace removed;
active-data hashes/timestamps unchanged across the probe.

Additional checks: `.venv/Scripts/python.exe -m py_compile
docs/control-plane/ledger/wo129_cli_probe.py` passed. Full regression command:
`.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider --basetemp
C:/Projects/qaos/.wo129-full-tmp`: 253 passed.

Only probe and records changed. Same-agent Reviewer checklist, not independent
review. Architecture-awareness kept this within existing public APIs and reused
WO-121 helpers. Product source/architecture is unchanged; architecture inspection
and import sweep remain WO-128 evidence, not rerun here. Unrelated dirty files,
providers and credentials untouched. No new blocker found. This verifies one
trusted deterministic app, not generalized app building or security isolation.
