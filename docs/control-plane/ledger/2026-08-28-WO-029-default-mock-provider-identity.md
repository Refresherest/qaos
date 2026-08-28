# WO-029 — Default Mock Provider Identity

## Objective

Resolve FINDING-004 so the built-in mock provider is registered under the
identity selected by default configuration and `AIEngine`.

## Architectural Context

`Configuration.ai_provider` and `AIEngine` both select `mock`. `MockProvider`
currently inherits the base-provider name `base`, so the default engine cannot
resolve it. The tracked callers establish `mock` as the intended built-in
identity.

## Scope

- Give `MockProvider` the explicit name `mock`.
- Add a direct default-engine generation/evidence regression test.
- Resolve FINDING-004 and update current-state records.

## Explicit Non-Goals

- Do not redesign the provider registry or AI engine.
- Do not add production providers or model resolution/governance.
- Do not modify Content OS behavior.
- Do not change credentials, active data, or unrelated findings.

## Acceptance Criteria

1. The built-in provider is registered as `mock`, not `base`.
2. A default `AIEngine()` resolves the built-in provider and generates the
   expected output and immutable evidence.
3. Explicitly injected-provider behavior remains unchanged.
4. Focused/full tests and standard verification pass; active data is unchanged.

## Stop Condition

Stop after FINDING-004 is resolved, reviewed, and published.
