# HANDOFF-009 — OpenHands Named Role-Profile Smoke Test

## Work Order

`WO-018` / `SMOKE-002`

## Status

`BLOCKED` before delegation

## Repository State Published for Test

- Repository: `C:\Projects\qaos`
- Branch: `feat/operational-builder-chain`
- Profile-binding commit: `11a6cb4`
- Remote: `origin/feat/operational-builder-chain`

The published mapping was:

| Stage | Primary and fallback profile |
| --- | --- |
| CSA | `QAOS_CSA` |
| PE | `QAOS_PE` |
| Reviewer | `QAOS_REVIEWER` |

## Fresh Cloud Run

One fresh OpenHands Cloud conversation was started with **No Repository
Connected**. The bounded prompt requested sequential delegation to
`qaos-csa`, `qaos-principal-engineer`, and `qaos-reviewer`, with no repository,
credential, provider-setting, or product-code changes.

## Exact Visible Failure

After the prompt was submitted, OpenHands displayed:

```text
Error occurred
Waiting for runtime to start...
```

No CSA output, `WORK_PACKAGE`, delegation event, named-profile lookup error,
PE output, Reviewer output, or repository change was observed. Browser console
inspection returned no warning or error text that further identified the
runtime-start failure.

## Stage Reachability

| Stage | Result |
| --- | --- |
| Parent runtime | Failed to start |
| CSA delegation | Not reached |
| PE delegation | Not reached |
| Reviewer delegation | Not reached |

## Restoration Decision

The required `model: inherit` restoration was **not** triggered. The observed
failure occurred before delegation and therefore is not evidence that a
delegated named profile failed to resolve. Restoring on this evidence would
silently misclassify a platform/runtime-start failure as a profile-store
failure.

## Changes and Safety

- No credentials were inspected or changed.
- No OmniRoute, provider, or OpenHands settings were changed.
- No QAOS product code or tests were changed.
- Unrelated pre-existing working-tree changes were preserved and excluded from
  the SMOKE-002 commits.

## Reviewer Outcome

`BLOCKED`

SMOKE-002 cannot establish named-profile delegation because the fresh
no-repository parent runtime did not start. This is not a rejection of the
published mapping and does not satisfy the condition for automatic
restoration.

## Stop Condition

Met. One fresh Cloud attempt was run and recorded. Do not retry or alter Cloud
settings without a new owner instruction or platform-state change.

## Continuation Preflight After Local Endpoint Allow Rules

The owner reported that RAV Endpoint Protection rules for the local Codex CUA
runtime processes had been changed to `Allow`. This was treated as a platform
state change authorizing one parent-runtime preflight before any further
SMOKE-002 delegation attempt.

A new **No Repository Connected** OpenHands conversation reached `Waiting for
task`. The following parent-only prompt was then submitted:

```text
Reply exactly: QAOS-PARENT-RUNTIME-OK
```

OpenHands again displayed:

```text
Error occurred
Waiting for runtime to start...
```

No model response, repository access, agent discovery, delegation, or named
profile resolution occurred. The repository-connected SMOKE-002 chain was
therefore not started.

This reproduction after the local allow-rule change does not establish that
RAV caused or did not cause the Cloud failure, but it makes the three QAOS
named bindings and repository-defined agents irrelevant to the observed
failure point. The next investigation must target OpenHands parent-runtime
startup evidence rather than changing QAOS agent files, profiles, credentials,
or provider settings.
