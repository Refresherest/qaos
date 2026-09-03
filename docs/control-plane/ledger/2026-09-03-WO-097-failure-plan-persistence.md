# WO-097 — Persist Plan on Ordinary Execution Failure

## Objective and Authority

Resolve FINDING-038 under the owner's next-step authorization. Baseline 462f2dd,
feat/operational-builder-chain. Plan retains canonical Task ownership;
ExecutionManager retains Objective lifecycle ownership.

## Scope

ExecutionEngine.execute, focused integration tests, and control-plane records.
Save current Plan transitions when queue.process raises, then rethrow the
original error even if cleanup persistence fails. Preserve successful execution
ordering and avoid saving on earlier planning/queue-construction failures.

## Non-Goals

No recovery preflight changes, historical data repair, migration, new public
APIs, provider changes, credentials, automatic retry, or unrelated fixes.

## Verification and Stop

Prove real execution failure produces coherent persisted Plan/Queue state;
reload and recover only failed/pending work. Cover cleanup-save failure and
original-exception identity. Run full regression, compile/import/architecture
checks and repeat WO-096 rehearsal. Record, commit, push, then stop.
