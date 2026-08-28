# FINDING-023 — Classifier Manager Global Dependency

## Status

`RESOLVED — WO-050`

## Evidence

ExecutivePipeline accepted an explicit classifier stage, and IntentClassifier
was already instantiable, but ClassifierManager always called the module
classifier. A caller could not carry a selected rule set through the manager
without replacing module state.

## Resolution

WO-050 allows ClassifierManager to retain an explicit IntentClassifier-compatible
service while preserving the existing module classifier as its default.

## Boundary

Classification rules, matching order, result vocabulary, persistence, and all
other executive stages are unchanged and not declared correct by this work order.
