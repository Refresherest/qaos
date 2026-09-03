# HANDOFF-089 — Recovery CLI Assessment

Baseline: 0a52f1f on feat/operational-builder-chain. Work order: WO-098.

PROPOSAL-011 defines one-shot recovery CLI semantics. DECISION-REQUEST-018
compares CLI recovery now, read-only ID inspection first, and remaining
programmatic. Option A is recommended; owner selection is required.

Only five ledger records and CURRENT_STATE/PROJECT_STATE changed. No product
code, test, runtime-data or unrelated change. See VERIFICATION-091.

Next: record the owner's selection. Implement only through a separately scoped
work order; keep unknown IDs fail-closed and do not infer UI, migration, or
automatic retry authority.
