# WO-028 — Content OS First Slice

## Objective

Implement and verify the bounded `Brief -> Reviewed Draft Artifact` vertical
slice authorized by OWNER-DECISION-001 and OWNER-DECISION-002, with readiness
Gates 4–5 as mandatory acceptance criteria.

## Architectural Context

Content OS owns brief validation and editorial review concepts. QAOS remains
the source for generic objective, plan, artifact, storage, and provider-neutral
generation infrastructure. Gates 1–3 are already proven.

## Scope

- A separate `content_os` package containing:
  - the approved six-field Brief;
  - `ACCEPT`, `REVISE`, and `BLOCKED` review outcomes;
  - immutable slice result/review values;
  - one explicitly composed first-slice service.
- Use one injected `Stores` collection for objectives, plans, and artifacts.
- Use the Gate 3 injected generation/evidence contract.
- Add a provider-interface test-only marker whose safe default is `False`.
- Focused success, invalid-input, provider-failure, and governance tests.
- Current-state, verification, and handoff records.

## Explicit Non-Goals

- No external publishing, channel credentials, calendars, campaigns, UI, SEO,
  analytics, retries, loops, or GPU workloads.
- No production provider/model selection or model governance designation.
- No multiple content formats or multiple artifacts per run.
- No changes to QAOS source-of-truth ownership.
- No repair of unrelated existing findings.

## Requirements

1. A valid brief creates one QAOS objective and one one-task plan.
2. Generation uses one explicitly injected test-only provider and captures the
   exact prompt/output evidence.
3. One generic QAOS artifact is stored and reviewed.
4. `ACCEPT` completes the task and objective and returns exactly one artifact.
5. Invalid briefs fail before objective creation or provider execution.
6. Provider failure returns a blocked result, persists failed task/objective
   state, and stores no artifact.
7. `REVISE` and `BLOCKED` remain bounded review outcomes with reasons.
8. Successful test generation does not change or imply model `VALIDATED` or
   `DESIGNATED` state, and no credentials enter source or evidence.

## Verification Requirements

- Focused first-slice tests
- Full regression suite and package-import sweep
- Compile and architecture inspection
- Active JSON content/mtime comparison
- JSON, secret-pattern, and whitespace checks

## Stop Condition

Stop after the first slice and Gates 4–5 are independently reviewed and
published. Do not continue into publishing, UI, retries, or a second slice.
