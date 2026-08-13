# QAOS Core Architecture Recovery Charter

## Owner direction

QAOS is being reconfigured from a part-right/part-wrong baseline. Earlier
architecture ADRs and reports are retained as drafts/evidence only, because
their originating direction may have incorporated incomplete memory or
hallucinated assumptions.

## Recovery rule

No module is "correct" because a draft says so, and no module is deleted
because an inspector flags it. Each core decision follows:

`observed behavior -> focused test -> owner-approved contract -> scoped change -> verification -> recorded result`

## First core boundary

The first reconfiguration target is the bootstrap/composition boundary:

- what may happen at package import;
- where configuration is created and owned;
- where services and registries are constructed;
- how a clean process obtains a runtime;
- what state is permitted to survive between runs.

This boundary is selected because current imports construct mutable singletons,
making all later architectural observations process-order dependent.

## Non-goals

- Do not normalize all registries or rename all duplicate classes at once.
- Do not assume a draft pipeline, persistence, or manager law is authoritative.
- Do not migrate durable data until a newly approved persistence contract exists.
