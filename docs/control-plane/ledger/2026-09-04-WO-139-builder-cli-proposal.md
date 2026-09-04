# WO-139 — Explicit Builder CLI Proposal

2026-09-04; baseline a95dc1a; feat/operational-builder-chain.
Authority: owner proceed on HANDOFF-118's proposal-only assessment.
Scope: this proposal, handoff and current-state records. No implementation.
Stop condition: evidence-backed options submitted for owner decision.

## Evidence and gap

WO-138/VERIFICATION-114 records nine fresh processes and 307 passing regressions.
Current src/qaos/application/session.py exposes execute_intent; planner/intents.py
owns PythonProjectIntentV2 and canonical metrics. main.py exposes objective,
objectives and recover, but no typed build submission. commands/objective.py
constructs a default session and executes a raw goal; commands/recover.py also
uses default permissions. Neither enables project generation. Existing CLI tests
protect these defaults. The builder is callable from Python, not directly from
an explicit end-user build command. Do not disguise raw-goal execution as typed
build authorization or claim that this is a general autonomous app builder.

## Option A — Explicit v2 build command (recommended)

Add a thin, separately approved command adapter, not a planner or new intent:

    python -m qaos.main build-project --workspace <state> --output-root <output> --directory Example --metrics words,lines --enable-project text_stats_project_v2

All five named options are required exactly once, in any order. Each takes one
value; reject unknown/duplicate/missing options, extra positional arguments,
empty values and option abbreviations. Metrics are exact lowercase comma-separated
enum tokens: no empty tokens, duplicates, implicit defaults or whitespace coercion.
Construct PythonProjectIntentV2 and reuse its normalization/validation. Require
the exact v2 enable token; command name, directory or metric selection alone is
not permission. The command is a local operator opt-in, not authentication or
a security boundary against an operator who can already execute Python.

Require explicit existing absolute state and output directories. Reject overlap
(equal or either ancestor) after resolution, and reject reparse traversal for
these command roots; preserve existing local Windows/fixed-NTFS output checks.
Do not create a missing root, select repository data by default, or change existing
API path policies. Parse/validate request, permission and roots before creating
stores/objectives. Root checks are bounded validation, not a new hostile-filesystem
sandbox or guarantee against concurrent filesystem replacement.

Use OperationalSession(create_stores(state), python_project_workspace=output,
enabled_python_projects=("text_stats_project_v2",)). Create one canonical
objective with a fixed internal planning goal and submit the typed intent; do
not interpret user prose. Print its ID immediately after creation. Report final
status and, on success only, published directory and normalized metrics. Existing
runtime log lines may remain; do not promise JSON-only stdout. Exit 2 for request
syntax/enum/permission errors, 1 for root/runtime/build failures, 0 only for a
completed build. Error output exposes exception type, never arbitrary payloads.
Collision remains an execution failure with coherent durable failure evidence;
never overwrite/adopt existing output. IDs must remain available after execution
failure when an objective was created.

Reuse current lifecycle, staged verifier, exact member digests and publication
checks. No second registry, persistence schema, renderer or capability. Preserve
all v1/v2 APIs and old command behavior. Existing objectives command discovers
the build; recover stays unprivileged and cannot recover project builds. Do not
silently add recovery permission flags or automatic retries in this work.

## Acceptance for a separate implementation work order

1. Parser tests cover every option, ordering, duplicates, unknowns, omissions,
   invalid metrics/enable token and early refusal without store/session writes.
2. Missing/relative/overlapping/reparse roots fail without creating roots or
   objectives. Exercise case-insensitive Windows path equivalence.
3. All seven selections map to the existing normalized typed intent and exact
   session permission. No raw-goal routing or default API permissions change.
4. Fresh-process CLI build, standalone selected-output use and objective discovery
   work with disposable roots; saved metrics and four digests match output.
5. Collision returns 1 with ID and coherent failed records, preserving original
   successful records/output. Root failure returns 1; malformed requests return 2.
   Inject sensitive exception text and prove it is not printed by the adapter.
6. Existing objective/recover defaults and v1 remain unchanged. Run focused/full
   tests, compile/import checks and architecture inspection. Active data and
   unrelated work must be preserved. No runtime-provider test is needed.

## Alternatives

Option B: constrained natural-language brief interpretation. More approachable,
but needs approved ambiguity/refusal rules and a review-before-execution boundary.
It is a larger requirement-to-intent change; defer until explicitly selected.

Option C: arbitrary generated-code projects. More expressive, but requires an
approved untrusted-execution boundary, independent acceptance and model governance.
Trusted-template verification does not establish those guarantees. Defer.

## Decision and verification

Approve, revise or reject Option A, including the new explicit CLI permission
and root constraints. OWNER-DECISION-028 does not authorize this CLI extension;
no new authority has been inferred. This proposal is complete, implementation
awaits a new owner decision. Architecture-awareness kept the CLI as a consumer
of the existing typed intent rather than a new source of truth.

Read-only architecture inspection with .venv/Scripts/python.exe (Python 3.14.3)
inspected 197 files and reported the same 22 existing findings; no fixes authorized.
307 tests are prior WO-138 evidence, not rerun for documentation-only work.
JSON/whitespace validation applies to these records. Product code, tests, active
data, dirty skills and untracked configuration/drafts/tools/test folders untouched.
Rollback is an owner-directed record revision, not a data/product migration.
