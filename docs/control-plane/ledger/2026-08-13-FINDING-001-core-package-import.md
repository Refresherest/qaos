# FINDING-001: `qaos.core` cannot import

- Status: resolved
- Severity: P0
- Classification: implementation-violation
- Governing authority: ADR-010; ADR-011B bootstrap/package laws
- Baseline: `f729c1b2ec24c28229d67d1135996ab365902534`, `main`

## Evidence

On 2026-08-13 UTC, the 44-package import sweep failed while importing
`qaos.core`. `src/qaos/core/runtime.py:1` imports `config` from `qaos.config`,
but `src/qaos/config/__init__.py` exports `configuration` instead. The exact
failure was `ImportError: cannot import name 'config' from 'qaos.config'`.

## Required response

WO-001 retained `configuration` as the canonical public name and updated
`qaos.core.runtime` to consume it directly. It added clean-process regression
tests for `qaos.config` and `qaos.core`; both pass. No compatibility alias was
introduced. See VERIFICATION-002.
