# OWNER-DECISION-029 — Explicit Builder CLI

2026-09-04. Authority: Qaasim April, repository owner.
The owner selected A in response to WO-139. Option A and its full permission,
root, compatibility and acceptance boundaries are approved for separate implementation.

Add build-project as a thin adapter to PythonProjectIntentV2 and OperationalSession.
Require exactly once each: --workspace, --output-root, --directory, --metrics and
--enable-project. The enable value must be text_stats_project_v2. Metrics use exact
comma-separated lowercase enum tokens and existing canonical normalization; no
defaults, empty tokens, duplicates, whitespace coercion or natural-language input.
Reject unknown/duplicate/missing options, abbreviations and extra positional values.

Require existing absolute state/output directories; reject overlap in either
direction, case-equivalent overlap and reparse traversal. Preserve local Windows/
fixed-NTFS output checks. Validate request, permission and roots before stores or
objectives are created. No default active-data root or missing-root creation.
This is explicit local operator opt-in, not authentication or a hostile-code sandbox.

Use the exact v2 session permission and a fixed internal planning goal; create
one canonical objective and print its ID immediately. Submit the typed intent,
report final status and successful published directory/normalized metrics.
Exit 2 for syntax/enum/permission errors, 1 for root/runtime/build failures and
0 only for completion. Adapter errors expose exception type, not payloads.
Existing runtime logs may remain. Preserve failure IDs and coherent failed records.

Reuse existing staging, verification, digests and no-replace publication. Preserve
v1/v2 APIs and old commands. Existing discovery remains usable; recover retains
default permissions. No recovery flags, retries, adoption, output editing, new
registry/schema/renderer/capability, providers, arbitrary code or Content OS expansion.

All six WO-139 acceptance requirements apply, including all-seven intent mapping,
early no-write refusals, fresh-process build/use/discovery, collision preservation,
sanitized errors, compatibility, full regression/compile/import checks and active
data preservation. Implementation is not yet completed or verified by this decision.
