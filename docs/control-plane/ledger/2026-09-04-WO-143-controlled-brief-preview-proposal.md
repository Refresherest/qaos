# WO-143 — Controlled Brief Preview Proposal

2026-09-04; baseline a91aad9; feat/operational-builder-chain.
Authority: owner next on HANDOFF-122. Scope: proposal/handoff/current-state
records only. Stop at owner decision; no implementation or new permissions.

## Evidence and assessment

commands/build_project.py parses explicit metric enums and directly submits an
existing PythonProjectIntentV2 to OperationalSession. planner/intents.py owns
metric validation, canonical order, directory restrictions and serialization.
No brief interpretation or preview path was found in commands/planner inspection.
WO-142 proves operator submission/use/refusal, not requirements understanding.

The smallest interpretation boundary is a pure, deterministic controlled-language
preview. It adds a reviewable requirement-to-intent mapping, not greater generated
app expressiveness. It must not be presented as general natural-language planning.
Its value is proving that interpretation can fail closed without becoming execution
authority. If broad app generation is the immediate priority, this alone is not it.

## Option A — Controlled-language preview only (recommended)

Proposed command:

    python -m qaos.main preview-project --directory Example --brief "count words and lines"

Require exactly --directory and --brief once each, either order, one value each.
Reject missing/duplicate/unknown/abbreviated options, extra positional values and
empty values. No workspace, output root, permission, execute or confirmation flags.

Define grammar version 1 as `count METRIC (and METRIC)*`, where METRIC is exactly
characters, words or lines. Require one to three distinct metrics. Input must be
a string of 1–256 characters containing ASCII letters and ordinary ASCII spaces
only. Permit ASCII case differences and repeated/leading/trailing spaces; lowercase
and split on spaces before matching the whole grammar. Reject tabs, newlines,
punctuation, Unicode lookalikes, synonyms, singular forms, duplicates, negation,
unknown clauses and extra instructions. No keyword extraction, partial matches,
defaults, fuzzy inference or fallback. Examples:

- `Count LINES and words` -> metrics [words,lines].
- `count characters` -> metrics [characters].
- `count words but not lines` -> refusal, not a guessed selection.
- `count words and publish it` -> refusal; no ignored suffix.

Pure planner-side interpretation constructs the existing PythonProjectIntentV2
using the separately supplied directory. Reuse its normalization and validation;
do not add another intent, registry or persisted specification schema. Directory
validation remains case-preserving and unchanged; do not interpret it from prose.

On success the command prints one JSON object and newline to stdout:

    {"status":"preview","grammar_version":1,"intent":<existing intent.to_dict()>}

No raw brief echo, generated source, shell command, objective ID or permission
fields. JSON key ordering need not be authoritative; the values and canonical
metric ordering are. Exit 0 means valid preview, never approved/completed build.
Invalid command/brief/directory exits 2 with a static grammar/usage diagnostic on
stderr and empty stdout. Unexpected failure exits 1 with exception type only.
Do not print arbitrary exception payloads or brief text in diagnostics.

Preview must not instantiate stores/session, inspect output roots, create an
objective, persist records, execute generated code or call a model/network service.
No QAOS data/output writes; routine Python bytecode effects are not application
persistence, and fresh-process no-write checks should use -B.

An operator reviews the displayed intent and separately invokes the already
approved build-project command with explicit roots, metrics and exact permission.
No automatic preview-to-build link, saved-preview loading, approval token, prompt
or implicit permission is added. This separation is a local workflow, not a new
identity/authentication boundary. Existing build validation always remains required.

## Separate implementation acceptance

1. Exhaust all 15 ordered nonempty unique metric sequences and their seven
   normalized selections; verify case/space variants and exact intent round trips.
2. Reject empty/overlong/wrong-type input, duplicates, malformed connectors,
   unknown words, punctuation, control characters, lookalikes and injected clauses;
   reject invalid directories under the existing intent contract.
3. Verify option order and all malformed options, exact JSON envelope, exit codes,
   empty stdout on refusal and static/sanitized diagnostics without input echo.
4. Prove preview never constructs stores/session or invokes execution/network;
   fresh -B subprocess success/refusal must leave disposable and active state/output
   unchanged and create no objective. No claim of a general hostile-code sandbox.
5. Compare preview intent to separately submitted typed build intent for a fixed
   disposable example; build retains explicit permission and output refusal rules.
   Do not add preview acceptance/loading to the build command.
6. Preserve old CLI/API/v1/v2 behavior; run focused/full tests, compile/import and
   architecture checks. Record proven behavior versus unsupported free-form language.

## Alternatives

Option B: model-assisted free-form brief interpretation with review. More flexible,
but requires separate model designation, ambiguity/refusal policy, workload evals,
data-handling boundaries and review/execution separation. Larger than A; no model
or provider readiness is inferred from earlier routing smoke tests.

Option C: retain explicit --metrics and prioritize a different builder capability.
Avoids adding a limited language interface. Reasonable if controlled-language
ergonomics are not useful, but leaves requirement interpretation untested. Would
require a separately selected capability proposal, not automatic scope expansion.

## Decision and verification

Approve, revise or reject Option A's exact grammar and preview-only boundary.
No interpretation is authorized by OWNER-DECISION-029. Architecture-awareness
kept existing intent ownership and separated preview from execution authority.
This proposal is complete; stop for owner decision before implementation.

Read-only architecture inspection: 198 files, same 22 existing findings. No
runtime tests rerun for docs only; 354 full regressions belong to WO-141, nine
walkthrough phases and 82 focused tests to WO-142. JSON/whitespace checks validate
records. No source/tests/data/provider changes; dirty skills and unrelated untracked
material preserved. Rollback is owner-directed record revision, not a migration.
