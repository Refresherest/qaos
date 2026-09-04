# OWNER-DECISION-028 — Configurable Trusted Project

2026-09-04. Authority: Qaasim April, repository owner.
The owner selects WO-135 Option A and approves its complete configuration,
versioning, permission and acceptance boundaries.

Add separately enabled text_stats_project_v2 with python_project intent version
2. Required metrics is a nonempty unique selection from characters/words/lines,
normalized to that order and copied/frozen. Reject invalid types, duplicates,
unknown values and extra fields; serialize as a canonical JSON array. No defaults.
The CLI returns exactly selected keys; the pure text_stats function retains its
full three-field API. Preserve existing input limits, self-test and error behavior.

Output remains four files: stats.py, app.py, test_stats.py, README.md. Only
validated enum literals may affect trusted rendering. Generated tests/docs and
execution evidence reflect the selection. Equivalent normalized requests produce
identical bytes across orderings and output directories. Preserve v1 source,
serialization and behavior unchanged. No automatic upgrade or inference from files.

Require exact v2 permission in empty-default enabled_python_projects and an
explicit project root; v1/file/template permission does not enable v2. Recheck
permission/configuration on reload/recovery. Reuse existing staged publication,
cleanup, collision refusal and publication-gap contracts, with no platform expansion.

A separate implementation work order must verify all seven configurations,
independent fixed acceptance, corrupted selected-key rejection, invalid-input
no-write behavior, immutability, determinism, v1 compatibility, recovery and
isolation, full regressions and fresh-process build/use/discovery. WO-135's
acceptance criteria apply in full.

No natural-language interpretation, models, arbitrary code, new dependencies,
output editing, automatic retries/adoption, UI, external deployment or Content OS
features are approved. No new specification registry or workflow engine.
