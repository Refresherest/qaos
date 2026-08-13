# RECOVERY-DECISION-002: Retire dormant parallel persistence

- Status: accepted by owner direction
- Date: 2026-08-13

`qaos.storage` remains the observed active persistence path: domain managers
use its stores directly. The separate `qaos.persistence` registry has no stores
and its only repository caller was a no-op pipeline save. It is retired without
changing active storage formats or existing domain-manager writes. A future
durable-state design requires a new evidence-backed decision.
