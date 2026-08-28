# DECISION-REQUEST-004 — Operational Composition Root

## Status

`OWNER DECISION REQUIRED`

## Evidence

WO-058 and WO-059 prove that existing QAOS services can form a fully isolated,
coherent Kernel-to-Capability runtime. The proof currently requires manual
construction of the complete dependency graph inside a test. No tracked source
names or specifies a production composition root for that graph.

The existing `create_runtime(configuration, ...)` is intentionally a low-level
service-container factory that accepts already-constructed services. Expanding
it silently would change its established core contract.

## Decision

Choose the public production composition boundary.

### Option A — Executive composition factory (Recommended)

Add a provider-neutral factory in the executive domain that accepts one explicit
Stores workspace and returns a fully composed ExecutiveManager. Callers retain
control of Configuration, Kernel, Dispatcher, logger, and event services.

Consequences:

- smallest new public boundary;
- preserves `create_runtime` and Kernel contracts;
- centralizes the proven domain dependency graph;
- callers still perform the final `Kernel(executive=...)` step.

### Option B — Operational Kernel factory

Add a higher-level factory that accepts a workspace root and returns a fully
composed Kernel.

Consequences:

- simplest application entry point;
- couples storage, configuration, dispatcher, runtime, and executive defaults;
- requires more policy choices now and creates a broader public contract.

### Option C — No production factory

Keep explicit construction solely at application/integration call sites.

Consequences:

- adds no public API;
- preserves maximum caller control;
- duplicates a large dependency graph and increases configuration drift risk.

## Recommendation

Select **Option A**. It turns the verified dependency graph into one reusable,
provider-neutral composition boundary without broadening core Runtime or Kernel.

## Explicitly Deferred

- exact optional override parameters;
- CLI/raw-goal entry points;
- provider/model selection;
- Content OS wiring;
- fallback, retry, and deployment policy.
