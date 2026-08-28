# DECISION-REQUEST-007 — Unclassified Objective Policy

## Status

`OWNER DECISION REQUIRED`

## Evidence

IntentClassifier returns `None` when an objective matches no registered
keyword. ExecutivePipeline stores that result and proceeds; classification is
not currently consumed by council delegation, planning, execution, reflection,
or learning.

The current rules cover architecture, design, plugin, code, review, delegate,
and objective keywords. They are not a complete natural-language intent model
and have never been designated as an execution authorization boundary.

## Decision

Choose the canonical behavior for unmatched objectives.

### Option A — Preserve `None` and Continue

Keep the current behavior and explicitly document `None` as a valid
classification.

Consequences:

- no runtime behavior change;
- broad goals continue to execute;
- callers and records must interpret null metadata consistently;
- absence of classification remains indistinguishable from classifier failure
  or missing policy.

### Option B — Assign `general_objective` and Continue (Recommended)

Make `general_objective` the canonical fallback returned only when no explicit
rule matches.

Consequences:

- preserves broad natural-language execution;
- removes ambiguous null classification from results and CLI output;
- keeps explicit keyword matches unchanged and deterministic;
- creates one new canonical classification value, but does not designate a
  provider, model, skill, or execution route.

### Option C — Reject Before Delegation

Treat an unmatched objective as a classification error and stop the pipeline
before council assignment or downstream persistence.

Consequences:

- provides fail-closed behavior;
- turns the keyword catalogue into an authorization gate;
- rejects reasonable goals lacking one of seven current keywords;
- requires explicit failure and objective-lifecycle semantics.

## Recommendation

Select **Option B**. `general_objective` honestly represents a valid broad goal
without making the incomplete keyword catalogue a safety gate. It improves
result determinism while leaving all explicit rules and execution routing
unchanged.

## Explicitly Deferred

- richer intent taxonomies or semantic classification;
- classification-driven skill, council, model, or provider routing;
- confidence scores and ambiguity handling;
- authorization, policy enforcement, fallback, retry, and deployment.
