# WO-014: OpenHands Operational Builder Chain

- Status: ready-for-cloud-validation
- Owner: Qaasim April
- Executor: QAOS Principal Engineer
- Authority: Owner direction to operationalize CSA -> PE -> Reviewer in OpenHands; `AGENTS.md`; `docs/control-plane/AI_EXECUTION_AND_HANDOFF.md`
- Scope: Add OpenHands file-based agent definitions, standardized handoff templates, explicit bounded fallback policy, and a parent orchestration instruction.
- Non-goals: Modify QAOS product code; designate QAOS models; store credentials; alter billing; claim the Cloud user interface has native automatic provider failover; submit a task that changes the repository; run an unbounded autonomous build loop.
- Affected paths:
  - `.agents/agents/*.md`
  - `docs/control-plane/templates/*_PACKAGE.md`
  - `docs/control-plane/OPENHANDS_BUILDER_CHAIN.md`
  - `docs/control-plane/ledger/2026-08-20-WO-014-openhands-builder-chain.md`
- Acceptance criteria:
  1. CSA, PE, Reviewer and one fallback per role are valid OpenHands file-based agents.
  2. Each agent has a role-appropriate tool set and explicit candidate model profile.
  3. The repository defines machine-readable handoff shapes and bounded remediation/fallback rules.
  4. No credential values or QAOS model designations are added.
  5. Agent frontmatter and Markdown files validate locally.
- Required owner validation: Pull this commit in OpenHands Cloud and run a no-op objective that requires CSA package generation and Reviewer verification but no product-code changes.
- Stop condition: Stop after repository validation and handoff. Do not launch a repository-changing autonomous task without a separate approved objective.

## Local Verification

- Six uniquely named agent files exist: CSA, PE, Reviewer, and one fallback per role.
- Each file contains the required OpenHands frontmatter fields: `name`, `description`, `tools`, and `model`.
- The allowed candidate model profile set is limited to `openai/deepseek-v4-pro`, `openai/qwen3-coder-plus`, and `openhands/glm-5.2`.
- Targeted scan found no credential-like assignment in the agent files or builder-chain protocol.
- `git diff --check` passed.

The workstation has no YAML parser installed. Do not add a parser dependency merely for this configuration check. OpenHands Cloud loading the files after the branch push is the required authoritative runtime validation.
