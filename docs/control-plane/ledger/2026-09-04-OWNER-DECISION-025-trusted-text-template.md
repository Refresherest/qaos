# OWNER-DECISION-025 — Trusted Text-Statistics Template

Date: 2026-09-04. Authority: Qaasim April, repository owner.

The owner selects WO-122 Option A and approves its behavior, acceptance and
safety boundaries. The first trusted template is text_stats_v1, generating one
importable Python module whose text_stats(text) returns character/code-point,
whitespace-token and splitlines counts. Non-string input raises TypeError;
the function performs no I/O.

A new python_template version-1 intent carries only relative output path and
the approved template ID. Source and independent fixed acceptance cases are
repository-owned. A guarded self-test entry reports success only after passing
the cases; corrupted behavior must be rejected. Preserve reproducible template,
version and source-digest evidence.

Require a separate explicit template-ID allowlist, empty by default, on factory
and session with an explicit confined output directory. Python-file opt-in alone
does not grant template authority. Reject unknown/disabled templates before
execution-state writes. Preserve PythonFileIntent v1, existing stored records,
atomic no-overwrite output and coherent failure/recovery.

A separate implementation work order may add the typed template contract,
trusted template/verifier, narrowly extend existing routing/composition/submission,
and add tests/records. Reuse Task, Plan, Queue and the existing pipeline.
No arbitrary code, model/provider work, shell/network/Git capability, publishing,
UI, migration, automatic retry or Content OS feature expansion is authorized.
