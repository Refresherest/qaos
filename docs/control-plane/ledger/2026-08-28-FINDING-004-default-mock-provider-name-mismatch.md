# FINDING-004 — Default Mock Provider Name Mismatch

## Status

`RESOLVED — WO-029`

## Evidence

- `AIEngine.__init__` selects the provider name `mock`.
- `MockProvider` does not override `AIProvider.name`, so its registered name is
  `base`.
- A default `AIEngine().generate(...)` therefore cannot resolve the built-in
  provider through the current registry.

## Impact on WO-025

The mismatch predates WO-025 and does not block the explicitly injected
provider path required by Gate 3. Named-provider compatibility is tested using
the provider's actual registered name.

## Disposition

WO-029 establishes `mock` as the built-in provider identity, consistent with
tracked configuration and `AIEngine`, and adds direct default-engine regression
coverage.
