# FINDING-006 — Memory String-Key Lifecycle

## Status

`RESOLVED — WO-031`

## Evidence

MemoryRegistry used `hasattr(title, "title")` to distinguish Memory objects
from strings in both `get` and `unregister`. Because `str.title` exists, string
keys became bound methods and could neither resolve nor remove memory entries.

## Resolution

WO-031 treats strings as canonical title keys and extracts `.title` only from
non-string entity objects. Immediate lookup, post-reload lookup, and persisted
string unregister are covered by focused tests.

## Boundary

No other registry is modified or implicitly declared correct by this result.
