# WO-004: Route CLI/kernel through explicit core construction

- Status: verified
- Priority: P0
- Authority: RECOVERY-DECISION-001
- Scope: kernel, dispatcher, CLI regression tests.
- Non-goals: rewriting legacy `qaos.runtime` or global subsystem managers.

## Evidence

`Kernel` previously constructed a duplicate `qaos.runtime.Runtime`, whose
source imports the removed global configuration and triggers broad bootstrap
side effects. The CLI therefore bypassed the recovered core boundary.

## Acceptance criteria

1. Kernel constructs the explicit core runtime and dispatches commands itself.
2. Command arguments reach handlers.
3. CLI help runs without legacy runtime bootstrap output.
4. Focused tests, full suite, import sweep, and inspection pass.

## Result

Kernel now creates the explicit core Runtime and dispatches commands directly.
Dispatcher forwards command arguments. The CLI help smoke test has no legacy
bootstrap output; focused tests pass (2), the full suite passes (8), and the
44-package import sweep passes.
