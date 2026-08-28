# WO-061 — Executive Composition Factory

## Objective

Implement OWNER-DECISION-004 as one reusable, provider-neutral Executive
composition boundary.

## Architectural Context

WO-058 and WO-059 verified the complete dependency graph through manual test
construction. OWNER-DECISION-004 authorizes Option A without changing Runtime
or Kernel construction authority.

## Scope

- Add `create_executive(stores, *, objectives=None, logger=None)`.
- Compose the verified classifier, council, planning, execution, reflection,
  learning, agent, skill, capability, worker, queue, and storage graph.
- Give each factory result isolated registries.
- Provide canonical isolated classifier and council-member construction.
- Export and test the public factory.

## Explicit Non-Goals

- No Runtime, Kernel, Dispatcher, CLI, raw-goal, provider, model, credential,
  Content OS, fallback, retry, deployment, or schema change.
- No automatic objective creation and no change to objective lifecycle rules.

## Verification Requirements

- Focused end-to-end factory test through Kernel.
- Objective, queue, plan, reflection, memory, and knowledge persistence checks.
- Global council registry isolation check.
- Full pytest, import sweep, compile, architecture inspection, JSON, secret,
  whitespace, and active-data checks.

## Stop Condition

Stop after the factory is implemented, independently reviewed, recorded, and
pushed. Do not begin a CLI or raw-goal entry point.
