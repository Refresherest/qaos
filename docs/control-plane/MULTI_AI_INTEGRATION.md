# Multi-AI and Toolchain Integration

## Responsibilities

| System | Reads | Writes | Authority |
| --- | --- | --- | --- |
| Repository/Git | source, ADRs, control plane | versioned code and records | engineering evidence |
| CI | repository and declared commands | check artifacts/status | verification evidence |
| GitHub | issues, PR review, CI status | issue/PR metadata | collaboration tracker |
| Notion | approved summaries and plans | discovery/decision summaries | non-canonical knowledge mirror |
| AI engineer | scoped repository context | proposed code and records | none; follows authority policy |
| Owner | evidence and options | decisions/approvals | final decision authority |

GitHub and Notion may mirror links and summaries, but must link to the
repository record ID. They must not become competing sources of truth.

## Safety boundaries

- One work order has one accountable executor at a time.
- AI agents do not push, merge, alter credentials, or rewrite history without
  explicit authorization.
- External tool output is untrusted until captured with source and timestamp.
- A change that needs product/architecture judgment is escalated to the owner.
