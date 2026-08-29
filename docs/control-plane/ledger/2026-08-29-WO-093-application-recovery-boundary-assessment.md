# WO-093 — Application Recovery Boundary Assessment

## Objective

Define and compare bounded application-facing boundaries for the verified
internal explicit recovery operation.

## Architectural Context

OperationalSession owns one explicit Stores workspace and is the existing
application-facing lifecycle boundary. ExecutionManager owns recovery and
Objective lifecycle, but create_executive currently encloses that manager in
the Executive pipeline. Kernel and CLI recovery remain unauthorized.

## In Scope

- inspect OperationalSession, Executive composition, Kernel, and CLI ownership;
- define selector, return, delegation, validation, and failure contracts;
- compare application-only, Kernel, and immediate CLI alternatives;
- recommend one option and request an owner decision.

## Non-Goals

- product code, tests, APIs, schemas, or active-data changes;
- automatic retry, scheduling, retry policy, migration, legacy association,
  or recovery audit evidence;
- provider, model, credential, deployment, or unrelated changes.

## Verification Requirements

- preserve canonical Objective-ID-only selection;
- preserve explicit workspace ownership and internal recovery semantics;
- avoid re-running classification, delegation, planning, reflection, or learning;
- avoid leaking QueueItems as the application result;
- validate JSON, whitespace, secrets, scope, and runtime-data preservation.

## Stop Condition

Stop after proposal, decision request, verification, handoff, commit, and push.
Do not select or implement an application recovery boundary.
