# WO-008: Make active JSON storage fail-safe

- Status: verified
- Priority: P1
- Scope: JSON decode failure handling and atomic file replacement.
- Non-goals: data migration, store construction refactor, schema redesign.

The current data files are readable, but malformed non-empty JSON is silently
returned as an empty list. This work makes corruption explicit while preserving
the existing empty-file initialization behavior and JSON data format.

## Result

`JSONStore` raises `StorageDataError` for non-empty corrupt JSON, creates parent
directories when saving, and atomically replaces the destination file. Focused
storage tests pass and the full suite passes (14 tests).
