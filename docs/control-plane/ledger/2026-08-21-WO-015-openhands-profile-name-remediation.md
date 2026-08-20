# WO-015: OpenHands Named Profile Remediation

- Status: ready-for-cloud-validation
- Owner: Qaasim April
- Executor: QAOS Principal Engineer
- Authority: Owner-approved no-code builder-chain smoke test; `AGENTS.md`; WO-014 runtime evidence.
- Objective: Correct the six OpenHands file-based agent `model` fields to use exact named Cloud profiles instead of raw provider/model IDs.
- Scope: Update only `.agents/agents/*.md`, `docs/control-plane/OPENHANDS_BUILDER_CHAIN.md`, and the relevant control-plane ledger records.
- Non-goals: Modify QAOS product code; add or change credentials; designate models; create or delete Cloud profiles; change the active Cloud default; run production work.

## Runtime Evidence

The Cloud smoke test delegated to `qaos-csa` and returned: profile
`openai/deepseek-v4-pro` not found. The same error class occurred for the
fallback. Cloud exposes profiles by names such as `QAOS-QwenCoderPlus`, not by
raw model identifiers.

## Approved Mapping

| Agent | Cloud profile name |
| --- | --- |
| `qaos-csa` | `QAOS-KimiK27Code` |
| `qaos-csa-fallback` | `QAOS-QwenCoderPlus` |
| `qaos-principal-engineer` | `QAOS-QwenCoderPlus` |
| `qaos-principal-engineer-fallback` | `QAOS-QwenCoderNext` |
| `qaos-reviewer` | `QAOS-QwenCoderNext` |
| `qaos-reviewer-fallback` | `QAOS-KimiK27Code` |

## Acceptance Criteria

1. Each of the six agents references an exact existing Cloud profile name.
2. The protocol table matches the agent files.
3. No credentials, raw credential values, or model designations are added.
4. Local frontmatter shape and secret scans pass.
5. A repeat no-code Cloud smoke test reaches all three roles or produces a new bounded runtime finding.

## Stop Condition

Stop after publishing the mapping and rerunning the no-code smoke test. Do not start QAOS product work.
