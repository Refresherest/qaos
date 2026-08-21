# HANDOFF-007: OpenHands Verified Primary Profile Remediation

- Status: ready for repeat Cloud validation
- Work order: WO-016
- Date: 2026-08-21

## Completed Change

The primary OpenHands Builder Chain assignments now use the exact named Cloud
profiles that each returned `PROFILE TEST OK` in an owner-run OpenHands test:

- `qaos-csa`: `QAOS-Deepseek-v4-pro-0813`
- `qaos-principal-engineer`: `QAOS-QwenCoderNext`
- `qaos-reviewer`: `QAOS-Deepseek-v3.2`

OpenRouter was not added or used. Existing fallback assignments were preserved
because they were not retested in the current Cloud configuration.

## Verification

- Primary agent frontmatter fields were checked locally.
- The three primary `model` values were checked against WO-016.
- The protocol table was updated to match.
- The changed scope was scanned for credential-like values.
- `git diff --check` passed.

## Required Owner Validation

Pull the latest branch state in OpenHands and rerun `SMOKE-001`. Success
requires the primary CSA, PE, and Reviewer agents to be reached and a final
Reviewer verdict returned without repository changes.

## Stop Condition

Do not start QAOS product work. Stop after the repeat smoke-test report.
