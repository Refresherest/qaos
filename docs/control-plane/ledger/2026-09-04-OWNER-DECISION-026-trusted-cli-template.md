# OWNER-DECISION-026 — Trusted Text-Statistics CLI Template

2026-09-04. Authority: Qaasim April, repository owner.

The owner selects WO-126 Option A and approves its documented interface,
acceptance gate and safety boundaries in full. This approves a separately enabled
text_stats_cli_v1 template generating one self-contained standard-library Python
file. Preserve text_stats_v1 and PythonFileIntent v1 without widening them.

The generated app accepts exactly one --text value (including empty; --text=VALUE
for leading dashes), limited to 4096 Unicode code points, returning only the
three JSON counts and a newline with exit 0. Invalid/missing/duplicate/unknown
arguments or oversized input exit 2 with a fixed bounded stderr diagnostic and
no stdout or echoed input. No arguments runs the guarded self-test; imports are
silent. Text-count semantics remain those of OWNER-DECISION-025.

No stdin, input files, output files, network, shell, dependency installation or
subprocess launch by the generated app. Command-line input is non-sensitive
because process listings and shell history can expose it.

Reuse the identity/path-only python_template v1 contract and existing pipeline,
Task/Plan/Queue ownership, confined workspace, exact-source integrity and atomic
no-overwrite lifecycle. The new ID needs separate explicit allowlist permission;
old-template or python-file permission does not grant it. Defaults remain empty.

A separate implementation work order may add this template and narrowly scoped
repository-owned CLI acceptance fixtures/verification hook. Fixed subprocess
argument arrays, shell=False, bounded timeouts/evidence, independently stated
expected results, corruption rejection, coherent failures, reload authorization,
fresh-process standalone use and full regression verification are required as
specified in WO-126. No caller-supplied commands/source/tests or general runner.

Multi-file packaging, model-generated code, providers, credentials, QAOS CLI
changes, UI and Content OS expansion remain outside this decision.
