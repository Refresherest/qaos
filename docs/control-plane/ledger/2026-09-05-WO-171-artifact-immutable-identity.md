# WO-171 — Artifact Immutable Identity, Digest and Provenance

2026-09-05; baseline `72a5945`; `feat/operational-builder-chain`.
Authority: OWNER-DECISION-035 selected Artifact option A1 and authorized this
separately scoped local implementation and independent-review stage.
Status: COMPLETE; independently accepted in VERIFICATION-122.

## Objective and architectural context

Evolve the existing provider-neutral Artifact domain rather than creating a second
candidate registry. Assign new artifacts immutable opaque IDs, derive an immutable
SHA-256 digest from their exact UTF-8 content bytes, retain bounded provenance, and
preserve legacy title lookup and missing-field loads without write-forward.

## In scope

- Add optional immutable `artifact_id`, derived `content_sha256`, and immutable
  bounded provenance to Artifact.
- Define canonical content bytes as strict UTF-8 encoding of Artifact's existing
  string content contract. Reject non-string content instead of inventing binary or
  multi-member canonicalization.
- Define provenance as at most 16 non-empty string key/value pairs, each key at most
  64 UTF-8 bytes, each value at most 1024 UTF-8 bytes, and at most 8192 canonical
  compact UTF-8 JSON bytes in total.
- Give ArtifactRegistry dual immutable-ID/latest-title indexes plus complete-record
  retention; reject duplicate non-null IDs before persistence.
- Make ArtifactManager inject IDs for new artifacts, persist new fields, retain all
  equal-title records, and expose exact ID and complete-record lookup.
- Preserve legacy records with absent ID, digest and provenance exactly when loaded
  and saved without mutation.

## Non-goals

- No binary or multi-member Artifact format, migration or active-data rewrite.
- No worker keys, users, SSH, sudoers, broker, networking or cloud changes.
- No candidate/source transfer, generated-code execution, QueueItem integration,
  model validation or designation.

## Verification

Focused tests must prove deterministic digesting, immutable identity/content/
provenance, equal-title retention, exact ID lookup, duplicate-ID refusal, provenance
bounds, and byte-for-byte logical legacy round-trip. Run relevant Content OS/storage
tests, the full regression suite, compile/import inspection, architecture inspection,
JSON parsing and whitespace checks. Confirm active Artifact data remains unchanged.

## Stop condition

Stop after implementation, verification, independent review and repository record.
Restricted transport setup remains a later separately authorized work order.
