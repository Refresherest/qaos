# OWNER-DECISION-030 — Controlled Brief Preview

2026-09-04. Authority: Qaasim April, repository owner.
The owner selected A in response to WO-143. Its exact grammar, preview-only
boundary and all six implementation acceptance requirements are approved.

Add preview-project with exactly --directory and --brief once each, either order.
Reject unknown/duplicate/missing/abbreviated options, empty values and extra
positionals. No workspace, permission, execution or confirmation flags.

Grammar version 1: count METRIC (and METRIC)*, with one to three unique metrics
from characters, words, lines. Brief must be a 1–256-character string of ASCII
letters and ordinary spaces only. Allow ASCII case and repeated/edge spaces;
normalize then match the whole grammar. Reject all unsupported text, duplicates,
punctuation, controls, Unicode lookalikes, synonyms, negation and extra clauses.
No guessing, partial matching or fallback. This is not free-form understanding.

Pure planner-side interpretation creates existing PythonProjectIntentV2 with
the separately supplied directory; retain existing validation, serialization and
canonical metric order. No new intent, registry or persisted specification schema.

Success: one JSON object plus newline, with status=preview, grammar_version=1,
and intent equal to existing intent.to_dict(). No raw brief, code, shell command,
objective ID or permission fields. Exit 0 means valid preview only. Invalid
request/brief/directory exits 2 with static usage/grammar stderr and empty stdout;
unexpected failure exits 1 with exception type only, never arbitrary payloads.

Preview cannot instantiate stores/session, inspect output roots, create objectives,
persist records, execute code or call models/network services. Use -B in fresh
process no-write checks to exclude routine bytecode caching. Review and build
remain separate: existing build-project requires explicit roots/metrics/permission.
No saved-preview loading, approval token, automatic build or implicit authority.

Verify all 15 ordered selections/seven canonical sets, grammar bounds/refusals,
option parsing, JSON/exit/redaction contracts, no execution/persistence/network,
fresh-process no-write behavior, separate preview/build intent equivalence,
compatibility, full regressions, compile/import and architecture checks as WO-143
specifies. No product implementation is claimed by this decision.
