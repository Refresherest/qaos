# WO-135 — Requirements-Driven Trusted Project Proposal

2026-09-04; baseline 9c2185d, feat/operational-builder-chain.
Authority: owner requested HANDOFF-114's next milestone assessment.
Scope: evidence, options, acceptance and decision request only. No product code,
provider/credential changes or new runtime permissions. Stop at owner decision.

## Baseline and gap

WO-133/134 prove staged four-file assembly, standalone execution, durable
discovery and safe refusal behavior. VERIFICATION-112 records 285 tests and the
nine-process rehearsal. planner/intents.py accepts identity/directory only;
capabilities/text_stats_project.py supplies fixed contents. These prove trusted
assembly, not planning arbitrary applications or adapting to user requirements.

The smallest functional next step is a constrained requirement that changes the
generated app's behavior, with exhaustive acceptance rather than another fixed
template differing only cosmetically. Larger remaining gaps include requirements
interpretation, general code synthesis, untrusted execution, revision workflows
and deployment. None is solved or authorized by this milestone.

## Option A — Explicit metric-selection project v2 (recommended)

Add separately enabled template text_stats_project_v2 and a new python_project
intent version 2. Carry template ID, the existing restricted directory name and
one required `metrics` selection. Allowed values are characters, words and lines;
require a nonempty unique selection. Reject unknown entries, duplicates, wrong
types and extra fields. Normalize valid selections to canonical order:
characters, words, lines. Copy/freeze input; caller mutation cannot change a build.
Serialized metrics are a JSON array in canonical order. No implicit defaults.

This gives seven valid configurations. The generated CLI returns exactly the
selected JSON keys and their counts. For example, metrics=["words"] and input
"hello world" returns {"words": 2}, not all three fields. Counts retain existing
semantics. Keep the pure text_stats function's full three-field API unchanged;
selection applies only to the app's output. Empty input, no-argument self-test,
4096-code-point limit and invalid-argument behavior retain existing contracts.

Output remains exactly stats.py, app.py, test_stats.py and README.md. Generated
tests and README describe the selection. No runtime configuration file, fifth
member, filenames supplied by the caller or new CLI flags. Source rendering may
use only validated enum literals; never arbitrary text/code interpolation.
Independent verifier expectations come from fixed literal case data plus the
approved selected keys, not generated code or a success marker alone.

Use existing project staging/publication/lifecycle, with per-file digests and
normalized metrics in existing execution evidence. Same normalized request must
produce identical bytes independent of input ordering or output directory.
Different selections must yield the appropriate distinct app/test/documentation
content and matching evidence. Preserve the project v1 serialized contract,
source bytes, full CLI output and behavior unchanged.

## Authority and scope boundary

Existing v1 project/file/template permission does not enable v2. Require the
exact v2 ID in empty-default enabled_python_projects with explicit project root.
Unknown/disabled versions or selections fail before execution-state writes.
Reload/recovery preserves configuration and rechecks v2 permission; it never
upgrades a persisted v1 intent or infers configuration from files.

This is a typed requirement, not natural-language interpretation. No LLM calls,
model designation, arbitrary code, new dependencies, edits to existing output,
automatic retry/adoption, platform expansion, UI, external deployment or Content
OS feature scope. Do not introduce a parallel specification registry or workflow
engine; the versioned intent and existing execution records carry this bounded
requirement. Architecture-awareness keeps the old contract separate from v2.

## Acceptance for separate implementation

1. Exercise all seven selections against literal ordinary/empty/multiline/Unicode
   cases. Check exact selected keys, counts and CLI stream/exit contracts.
2. Reject empty/duplicate/unknown/invalid selections and extra serialized fields
   without state writes. Test caller mutation, normalization and round trips.
3. Prove deterministic bytes for equivalent selection orderings and different
   directories; recorded configuration and member digests match generated files.
4. Corrupt selected-key behavior while retaining self-test success; independent
   acceptance must reject before publication and preserve coherent failure.
5. Verify v1 compatibility, v1-only denial of v2, reload permission/configuration,
   collision refusal, cleanup, publication-gap behavior and workspace isolation.
6. Run full regressions, compile/import checks and a fresh-process configurable
   build/use/discovery rehearsal; active data and unrelated changes unchanged.

## Alternatives

Option B: natural-language brief to the existing fixed template. Potentially
more approachable, but requires a separately approved interpretation/ambiguity
contract; does not itself prove generated behavior changes. Defer until the
bounded typed requirement can be reliably executed and verified.

Option C: arbitrary model-generated projects now. Closer to the eventual broad
builder, but requires designated models, independent acceptance and an approved
untrusted-code execution boundary. Existing trusted-template tests are not that
evidence. Defer to a separate architectural/risk decision.

## Decision requested

Approve, revise or reject Option A and its configuration/version/permission
boundaries. This proposal is complete; implementation remains separate.
No runtime tests rerun for this documentation-only work order. The 285-test
baseline belongs to WO-134. JSON/whitespace checks verify records only. Unrelated
dirty skills and untracked material preserved. Rollback is owner-directed
revision of proposal records, not a product/data migration.
