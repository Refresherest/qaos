# QAOS Architecture Inspection

- Generated: 2026-08-13T13:36:47+00:00
- Commit: `f729c1b2ec24c28229d67d1135996ab365902534` on `main`
- Python files inspected: 195
- Working-tree entries: 34

## Findings

| ID | Severity | Classification | Governing rule |
| --- | --- | --- | --- |
| DUPLICATE-CLASS-AGENT | P2 | review | ADR-001 / ADR-005A canonical object law |
| DUPLICATE-CLASS-CAPABILITY | P1 | review | ADR-001 / ADR-005A canonical object law |
| DUPLICATE-CLASS-JSONSTORE | P2 | review | ADR-001 / ADR-005A canonical object law |
| DUPLICATE-CLASS-MEMORY | P1 | review | ADR-001 / ADR-005A canonical object law |
| DUPLICATE-CLASS-OBJECTIVE | P1 | review | ADR-001 / ADR-005A canonical object law |
| DUPLICATE-CLASS-RUNTIME | P2 | review | ADR-001 / ADR-005A canonical object law |
| DUPLICATE-CLASS-SERVICECONTAINER | P2 | review | ADR-001 / ADR-005A canonical object law |
| DUPLICATE-CLASS-TASK | P1 | review | ADR-001 / ADR-005A canonical object law |
| REGISTRY-ACTIONS | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-AI | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-ARTIFACTS | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-BOOTSTRAP | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-CLASSIFIER | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-COMMANDS | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-CONTAINER | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-COUNCIL | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-EVENTS | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-EXECUTION | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-EXECUTIVE | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-KNOWLEDGE | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-PERSISTENCE | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-PLUGINS | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-QUEUE | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-SCHEDULER | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-TASKS | P2 | implementation-violation | ADR-003 / ADR-005 |
| REGISTRY-WORKFLOWS | P2 | implementation-violation | ADR-003 / ADR-005 |
| ENTITY-OBJECTIVE-SELF-PERSISTENCE | P1 | implementation-violation | ADR-001 / ADR-008A / ADR-011J |
| IMPORT-TIME-MUTABLE-SINGLETONS | P1 | implementation-violation | ADR-010 / ADR-011E |

## Limitations

- Static evidence only; runtime behavior, data migrations, and semantic ownership require targeted tests/review.
- A finding is not authorization to modify code. Follow the control-plane work-order process.
