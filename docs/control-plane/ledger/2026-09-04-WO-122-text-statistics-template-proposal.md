# WO-122 — First Useful Deterministic Workload

Baseline ebed784, feat/operational-builder-chain, 2026-09-04.
Scope: assess and propose one workload beyond print-only. No implementation,
provider calls, relaxed validation, executable permission or product change.

## Evidence

WO-121 proves public submission and durable state across processes, but
PythonFileIntent accepts only one literal print expression. Its validation,
serialization, routing and caller opt-in must not silently change meaning.
The next workload should demonstrate real reusable behavior, not merely a
different printed string, while retaining deterministic acceptance.

## Option A — Explicit trusted text-statistics template (recommended)

Generate one importable Python module exposing `text_stats(text)` that returns
`characters`, `words` and `lines` for a supplied string. Contract:

- characters: Python string length (Unicode code points, not grapheme count).
- words: number of whitespace-separated tokens using str.split; not linguistic
  segmentation or SEO analysis.
- lines: number of str.splitlines entries; empty text has zero lines and a
  terminal newline does not introduce another line.
- Non-string input raises TypeError. The function performs no I/O.

Use a new versioned template intent (`python_template`, version 1), carrying a
relative output path and the exact template identifier `text_stats_v1`. No
caller-supplied source, commands, test code or expected result is accepted.
Source and acceptance fixtures come from reviewed repository-owned templates.
Do not widen PythonFileIntent v1 or infer template authorization from its type.

The generated module contains the function plus a guarded self-test entry that
runs fixed cases and emits one deterministic success marker only if all pass.
Acceptance covers empty text, ordinary words, repeated whitespace, multiple
lines, CRLF, a trailing newline, Unicode and non-string input. Fixtures must
contain independently stated expected values, not values computed with the
same implementation being tested. Test deliberately corrupted generated
behavior to prove verification rejects it rather than trusting its marker.

## Explicit authority and implementation boundary

Require a separate opt-in allowlist of template identifiers on the factory and
session (empty by default), alongside an explicit confined output directory.
Existing python_file_workspace opt-in alone must not authorize template work.
Unknown identifiers/versions and disabled templates fail before execution-state
writes. Existing print-only behavior and serialized records remain unchanged.

Reuse Task identity, PlannerManager-owned one-task Plans, explicit skill routes,
Queue/evidence and the six-stage session pipeline. No duplicate orchestration.
A separate implementation work order may add this one typed template contract,
trusted template/verifier, narrowly extend routing/composition/submission and
tests. Preserve atomic no-overwrite output, bounded verification and coherent
failure/recovery. Exact source generation and template/version/digest evidence
must be reproducible. New template output must remain confined and opt-in.

This is a generic text utility that a future Content OS could consume, not a
Content OS feature or claim that QAOS can autonomously design applications.
No models, arbitrary Python, shell, network, dependency installation, Git,
publishing, UI, migration or automatic retry is authorized.

## Alternatives

Option B: broaden the existing AST allowlist to arbitrary functions and control
flow. Reject for this step: much larger execution/safety scope and changes the
print-only contract's meaning.

Option C: add live model-generated code immediately. Defer: model designation,
untrusted-code execution and independent verification require separate authority.

## Owner decision requested

Approve, revise or reject **Option A: an explicitly enabled trusted
text_stats_v1 template**, with the behavior and safety boundaries above.
Implementation remains separate. No tests rerun for this documentation-only
assessment; the executable baseline remains WO-120's 223 tests plus WO-121's
fresh-process rehearsal. Unrelated changes are preserved.
