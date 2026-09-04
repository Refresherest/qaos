# VERIFICATION-112 — WO-134

2026-09-04; baseline 70c1db3. Outcome: ACCEPT WITH NOTES.

`.venv/Scripts/python.exe docs/control-plane/ledger/wo134_project_probe.py`
completed successfully. Nine fresh top-level processes: build, app use, generated
tests, discovery, collision build, default recovery, old-template recovery,
project-root-only recovery and authorized recovery. Exit codes:
0, 0, 0, 0, 1, 1, 1, 1, 1. The 1 codes are probe-defined caught refusals, not
new QAOS CLI behavior. Build additionally runs the existing 17 verification
children; these are not included in the top-level count.

Published member set is exactly stats.py/app.py/test_stats.py/README.md. Recorded
SHA256 digests match output; all 15 CLI cases passed during build. Standalone
execution uses -E -s -B to ignore Python environment/user site and suppress
bytecode while retaining local cross-file imports. App counts and generated
test marker match expected values. Discovery records completed status.

Use/tests/discovery and all three permission denials preserve workspace file
hashes/timestamps. Collision and authorized recovery raise FileExistsError.
Objective/Plan Task/QueueItem/action remain coherently failed. Original successful
records and all project output are preserved, with no residual staging directory.
Validated disposable root removed; active data unchanged across the probe.
Probe py_compile passed.

Full regression: `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider
--basetemp C:/Projects/qaos/.wo134-full-tmp`: 285 passed in 67.80s.
JSON parsing and Git whitespace checks pass for the records.

Same-agent Reviewer checklist, not independent delegation. Architecture-awareness
kept this within existing APIs and reused WO-121 fingerprint/record helpers.
No product code, providers, credentials or unrelated changes. Scope remains local
Windows/NTFS trusted generation, not arbitrary applications or security isolation.
Architecture inspection/import sweep remain WO-133 evidence, not rerun here.
