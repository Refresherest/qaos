# OWNER-DECISION-004 — Operational Composition Root

## Status

`ACCEPTED`

## Decision

The owner selected **Option A — Executive composition factory** from
DECISION-REQUEST-004.

QAOS may add a provider-neutral executive-domain factory that accepts one
explicit Stores workspace and returns a fully composed ExecutiveManager.
Callers retain final control of Configuration, Kernel, Dispatcher, logger, and
event services.

An optional ObjectiveManager injection is permitted so objective creation and
lifecycle persistence can share one explicit registry. The factory must use
isolated registries and must not alter provider, model, credential, CLI,
raw-goal, Content OS, fallback, retry, or deployment policy.
