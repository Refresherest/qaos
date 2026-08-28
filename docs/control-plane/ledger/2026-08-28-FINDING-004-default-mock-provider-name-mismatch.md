# FINDING-004 — Default Mock Provider Name Mismatch

## Status

`OPEN — OUTSIDE WO-025`

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

Do not repair this mismatch under WO-025. If prioritized, issue a separate
work order that defines the intended built-in provider identity and verifies
all affected callers.
