# FINDING-016 — Command Dispatcher Global Mapping

## Status

`RESOLVED — WO-041`

## Evidence

Every Dispatcher read the module-level COMMANDS mapping, and Kernel always
constructed Dispatcher internally. A bounded runtime command surface required
monkeypatching global state.

## Resolution

WO-041 adds explicit command-map injection to Dispatcher and dispatcher
injection to Kernel, retaining the existing mapping and dispatcher as defaults.

## Boundary

Command names, handlers, CLI help, Runtime/executive routing, and command-domain
semantics remain outside this work order.
