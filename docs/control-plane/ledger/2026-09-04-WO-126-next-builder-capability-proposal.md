# WO-126 — Next Builder Capability Proposal

2026-09-04; baseline 69493a6, feat/operational-builder-chain.
Authority: owner requested the proposal identified by HANDOFF-105.
Scope: repository evidence, options, acceptance gate and decision request only.
Non-goals: implementation, expanded execution authority, providers or credentials.
Stop condition: record proposal and handoff; request owner approval.

## Evidence and architectural context

WO-124/125 establish one explicitly enabled trusted module, fresh-process use,
durable discovery, collision refusal and disabled recovery without writes.
VERIFICATION-107 records 245 passing tests. Inspected planner/intents.py,
capabilities/python_file.py and capabilities/python_template.py under src/qaos.
The current capability executes exactly one generated file with no arguments;
the template performs its self-test on that path. Task/Plan/Queue ownership,
explicit routing, source digest and no-overwrite lifecycle already exist.
This is not yet evidence of an end-user application or generalized app building.

## Option A — Trusted single-file text-statistics CLI (recommended)

Add a separately enabled template ID `text_stats_cli_v1`, not a silent change to
text_stats_v1. Generate one self-contained Python file with the existing pure
text_stats function and a small argument-to-JSON interface. No QAOS installation
is required to use the generated file; Python standard library only.

Proposed generated-app contract:

- `python generated.py --text "hello world"` emits one JSON object with exactly
  characters=11, words=2, lines=1, followed by a newline, and exits 0.
- Exactly one `--text` value is accepted (including empty string); use
  `--text=VALUE` for text beginning with a dash. Values are data, never code.
- Maximum 4096 Unicode code points. Missing text, duplicate/unknown arguments,
  and oversized input exit 2, emit a fixed bounded diagnostic to stderr and no
  stdout. No input text is echoed in diagnostics.
- With no arguments, retain the builder's existing guarded fixed self-test
  path and emit the template-specific success marker only after acceptance.
  Import emits nothing; text_stats semantics remain those in OWNER-DECISION-025.
- No input-file reads, stdin, output-file writes, network, shell, dependency
  installation or subprocess launch by the generated application. It only reads
  its arguments and writes counts or diagnostics to standard streams.
- Command-line text may be visible in process listings or shell history. This
  first interface is for non-sensitive text, not secret/private-content handling.

Reuse python_template v1's identity/path-only contract, existing one-task Plan,
capability routing and confined output workspace. Caller arguments, source,
expected values and test code must NOT become new intent fields. Authorizing
text_stats_v1 or python_file alone must not authorize text_stats_cli_v1.
Require its exact ID in the empty-by-default per-session/factory allowlist.
Keep old serialized records, source bytes and default behavior compatible.

## Acceptance gate for a separately authorized implementation

1. Public session generates the new file and records template ID/version/digest.
2. Independent fixed CLI subprocess cases verify JSON keys/counts, exit codes
   and stdout/stderr separation, including empty text, multiline, Unicode,
   leading dash, 4096/4097 boundaries and invalid arguments.
3. Fixed argument arrays use shell=False, existing bounded timeouts and bounded
   evidence. Acceptance values are reviewed constants, not recomputed with the
   implementation. A success marker alone is insufficient: corrupt CLI behavior
   must cause builder verification failure and coherent failed state.
4. Unknown/disabled IDs reject before execution-state writes, including reload;
   exact-source integrity, confinement, collision refusal and isolation persist.
5. Fresh-process generated-app use works without importing QAOS. Existing 245
   tests plus new tests, compile checks and active-data preservation pass.

A future implementation may narrowly add repository-owned CLI fixtures and a
template-specific verification hook to the existing capability lifecycle. It
must not create a general command runner or duplicate orchestration. This is
the explicit proposed expansion beyond the current no-argument verifier.

## Alternatives and consequences

Option B: trusted multi-file package. Better evidence of project structure and
cross-file imports, but needs separately defined all-or-nothing publication,
partial-failure/recovery, path ownership and package verification. Defer until
those contracts are approved; current atomic creation covers only one file.

Option C: model-generated applications now. Broader flexibility, but requires
model designation, untrusted-code isolation and independent acceptance authority.
Not justified by the deterministic-template evidence; defer to separate decisions.

## Decision and verification status

Approve, revise or reject Option A and its generated-app interface and safety
boundaries. Approval does not imply multi-file, arbitrary code, QAOS CLI changes,
UI, Content OS feature or provider authority. No implementation occurred.
Documentation-only review; regression tests were not rerun. Executable evidence
remains VERIFICATION-107, not a claim of new verification. Unrelated modified
skills and untracked configuration/drafts/test directories are preserved.
Rollback is removal/revision of these proposal records only; no data migration.
