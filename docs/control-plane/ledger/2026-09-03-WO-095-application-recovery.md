# WO-095 — Application Recovery

## Objective and Architecture

Implement OWNER-DECISION-017: OperationalSession owns the explicit workspace,
ExecutiveManager delegates recovery, and ExecutionManager retains lifecycle
and recovery ownership.

## Scope and Requirements

- Add canonical-ID-only `OperationalSession.recover_objective` returning its
  canonical Objective after success.
- Share the factory's ExecutionManager between pipeline and recovery service.
- Delegate directly without running any normal Executive pipeline stage.
- Preserve existing constructors and execution behavior; missing recovery
  service fails explicitly without falling back to global services.
- Change only session, Executive manager/factory, tests, and control-plane records.

## Non-Goals

Kernel, CLI, UI, internal recovery semantics, migration, automatic retry,
providers, credentials, audit evidence, and unrelated edits remain unchanged.

## Verification and Stop Condition

Test delegation, success after reload, failure propagation, invalid selectors,
workspace isolation, and pipeline bypass; run regression, compile, import,
architecture and scope checks. Record results, commit and push, then stop.
