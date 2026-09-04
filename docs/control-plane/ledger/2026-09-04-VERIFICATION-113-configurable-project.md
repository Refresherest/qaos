# VERIFICATION-113 — WO-137

2026-09-04; baseline 8858230. Outcome: ACCEPT WITH NOTES.

Implemented PythonProjectIntentV2, required normalized immutable metrics and
text_stats_project_v2 opt-in. Existing factory/session project allowlist is reused;
Executive recovery, PlannerManager, Task serialization and exact resolver routing
recognize the new typed version. No separate registry, storage or workflow engine.

The trusted v2 renderer uses only validated enum literals. stats.py remains v1's
pure full-count API; app.py selects output keys; generated tests/README reflect
selection. Per-call capability copies hold immutable rendered members/configuration,
avoiding leakage into v1 or other builds. Existing publication/cleanup/refusal
path is shared. Fixed CLI expectations filter independently stated count fixtures
by approved keys; generated code is not the acceptance authority.

Verification using .venv/Scripts/python.exe:

- Initial focused collection failed because a test helper was imported as a
  sibling module; replaced with local test helpers without changing product code.
- `-m pytest tests/test_configurable_project.py -q -p no:cacheprovider --basetemp
  C:/Projects/qaos/.wo137-focused-fixed-tmp`: 20 passed before two additional tests.
- `-m compileall -q src tests`: passed.
- Final `-m pytest -q -p no:cacheprovider --basetemp C:/Projects/qaos/.wo137-full-tmp`:
  307 passed in 160.64s; active-data hashes/timestamps unchanged across the run.
- pkgutil/import sweep: 195 QAOS modules imported.
- `tools/architecture_inspect.py`: 197 files; existing duplicate/registry/singleton
  findings remain outside scope.
- Git comparison of text_stats_project.py, text_stats_template.py and
  text_stats_cli_template.py: unchanged from baseline.

Coverage includes seven builds with all 15 fixed CLI cases each, plus independent
ordinary/empty/multiline/Unicode subprocess cases; invalid/duplicate/wrong-type
metrics; normalized order, caller mutation and serialized round trips; rendered
byte determinism across input order/output directories; distinct app/tests for
all selections; mixed v2/v1 session; v1-only permission denial; corrupted selected
output rejection even though generated tests/no-argument self-test pass; cleanup,
reload of saved configuration, authorized recovery, collision and publication-gap
refusal; workspace isolation and corrupted in-memory intent no-write rejection.
Fresh-process build, standalone selected-output use and read-only discovery pass.

Same-agent Reviewer checklist, not independent delegation. Architecture-awareness
kept v1 authority/bytes distinct and reused existing lifecycle owners. No providers,
credentials, arbitrary-code path, platforms, UI or active migration. Local Windows/
NTFS and previous crash-gap/hostile-filesystem limitations remain. Per-child
timeouts are unchanged; no five-second total build claim. Unrelated working-tree
changes and untracked test artifacts preserved.
