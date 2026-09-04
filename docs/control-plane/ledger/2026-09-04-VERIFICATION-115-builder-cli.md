# VERIFICATION-115 — WO-141

2026-09-04; baseline 5d13fc3; Python 3.14.3; Windows/local NTFS.
Outcome: ACCEPT WITH NOTES. Same-agent review, not independent delegation.

Implemented commands/build_project.py with strict required option pairs, exact
v2 permission, existing intent normalization and root validation before stores.
main.py adds dispatch and help only. Existing application, intent, capability,
renderer and recovery code remain unchanged. No new canonical concept or registry.
Architecture-awareness kept the adapter as a consumer of the existing typed API.

Commands using .venv/Scripts/python.exe:

- `-m pytest tests/test_build_project_cli.py -q -p no:cacheprovider --basetemp
  C:/Projects/qaos/.wo141-focused-tmp`: 46 passed in 10.73s before one additional
  test for all 120 option orders, abbreviations and option-as-value rejection.
- `-m pytest -q -p no:cacheprovider --basetemp C:/Projects/qaos/.wo141-full-tmp`:
  354 passed in 166.73s; active-data hashes/timestamps unchanged across suite.
- `-m compileall -q src tests`: passed after final source/test edits.
- pkgutil.walk_packages plus importlib.import_module: 196 QAOS modules imported.
- `tools/architecture_inspect.py`: 198 files, same 22 pre-existing findings.
  Findings are not authority to refactor unrelated code.

47 new tests cover missing/duplicate/unknown/blank options, all option orders,
exact permission, malformed metrics, all-seven normalized intent/session mappings,
ID printed before execution, early missing/relative/file/overlapping roots,
Windows case-equivalent overlap and simulated reparse attributes for both roots.
Reparse tests exercise the shared guard with mocked lstat attributes, not a new
real-junction experiment. Existing filesystem capability regression coverage remains.
Runtime exception payload redaction and non-completed results cannot report success.

Fresh subprocesses build through the real CLI, execute the standalone selected
app, discover the objective, refuse collision and refuse default recovery. Four
member digests match evidence; normalized metrics persist; original successful
records/output are unchanged; failed objective/plan/queue status is coherent.
No read-only discovery/recovery writes or active-data changes were observed.

Scope: new adapter and test file, main.py routing/help, three ledger records and
two current-state records. Existing tests and v1/v2 product implementation untouched.
Dirty skills, untracked configurations/drafts/tools/prior test artifacts preserved;
new focused/full-suite test artifacts left untracked. No provider, credential,
OpenHands, arbitrary-code or active-data migration changes. Root validation is
not protection against concurrent hostile filesystem replacement. Error payload
redaction applies to the adapter; existing runtime logging remains unchanged.
Known .pytest_cache access warning is unrelated and was not repaired.
JSON and Git whitespace checks apply to final records before checkpoint.
