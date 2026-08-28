# WO-025 — Deterministic Generation Contract

## Objective

Establish and verify the provider-neutral, explicitly injected deterministic
generation contract required by Content OS readiness Gate 3.

## Architectural Context

QAOS already defines `AIProvider.generate(prompt)` and an `AIEngine` that uses a
globally registered provider name. PROPOSAL-004 requires a future slice to
inject a deterministic provider without changing global provider/model state
and to retain its prompt and generated output as execution evidence.

This work order establishes that QAOS-level boundary only. It does not build
the Content OS slice or select a production provider/model.

## Approved Contract

1. `AIEngine(provider=...)` accepts an explicit provider instance scoped to
   that engine.
2. Explicit injection does not register, select, or mutate a global provider.
3. `generate_with_evidence(prompt)` invokes the selected provider once and
   returns immutable evidence containing the exact prompt and output.
4. Existing `AIEngine().generate(prompt)` behavior and the default global
   engine remain compatible.
5. Calling `use(provider_name)` explicitly returns an injected engine to the
   existing named-registry resolution path.

## Scope

- `src/qaos/ai/engine.py`
- One provider-neutral generation-evidence value object and public export
- Focused deterministic-generation tests
- Current-state, verification, and handoff records

## Explicit Non-Goals

- Do not implement Content OS briefs, artifacts, reviews, or workflows.
- Do not modify execution, planning, task, artifact, or objective behavior.
- Do not add production providers, model resolution, retries, or credentials.
- Do not infer model `VALIDATED` or `DESIGNATED` state.
- Do not implement Gates 4–5.

## Acceptance Criteria

1. An unregistered deterministic test provider can be injected and used
   without changing the provider registry or default engine selection.
2. Evidence captures the exact prompt and output and provider execution occurs
   exactly once.
3. Evidence is immutable.
4. Existing named-provider and `generate(prompt)` behavior remains compatible.
5. Active `data/*.json` content and modification times are unchanged.
6. Focused and full regression tests, compilation, package imports,
   architecture inspection, JSON, secret, and whitespace checks pass.

## Stop Condition

Stop after the Gate 3 contract is published and reviewed. Do not continue into
end-to-end success/failure or governance proof under Gates 4–5.
