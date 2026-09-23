# Change: Adopt Python-Native Text and Number Semantics

## Why

The migration to Python kept three JavaScript behaviors so the port could match the TypeScript reference exactly: JavaScript's whitespace set for blank checks, JavaScript number spelling in duplicate-sequence messages, and the `Number.MAX_SAFE_INTEGER` sentinel for unsequenced trace events. Python is now the only implementation, and nothing depends on those JavaScript details. Emulating them adds code (`lasm_core._js`) and surprises Python maintainers. This change adopts Python semantics.

## What Changes

- Required-string and trace-actor blank checks use `str.strip()`. `\x1c`–`\x1f` and `\x85` count as blank; a lone `﻿` counts as content.
- Unsequenced trace events sort after every numbered event, then by input order. An explicit sequence of 9007199254740991 no longer ties with unsequenced events.
- Duplicate trace sequences compare as numbers (`1` and `1.0` collide) and are reported with Python spelling (`Duplicate id: 1e-07`).
- Integer-valued floats remain valid integer sequences. JSON does not distinguish `2` from `2.0`, and the interchange contract treats numeric spelling as non-semantic.
- The TypeScript reference corpus remains unedited. Each intentional difference is recorded in `tests/corpus/deviations.json` with a reason and a JSON Patch, and the parity test applies it.
- Finding codes, paths, message templates, event vocabulary, and all other ordering and evaluation behavior are unchanged.

## Impact

- Affected capability: `establish-auto-bench-sans-io-core` (Agentic Trace Model and Migration Behavioral Parity requirements).
- Affected code: `src/lasm_core/validate.py` and `src/lasm_core/trace.py`. `src/lasm_core/_js.py` is removed.
- Affected tests and docs: `tests/corpus/deviations.json`, `tests/corpus_support.py`, `tests/test_parity.py`, `tests/test_trace.py`, the corpus provenance and verification notes, the migration guide, the API inventory, and the project context.
- Behavior differs from `@lasm/core` 0.1.0 only for the inputs above: 6 of 129 reference cases.

## Supersedes

- `migrate-lasm-core-to-python` — replaces its requirement to preserve the TypeScript omitted-sequence sentinel and exact reference parity. Parity with the TypeScript record now allows reviewed, documented deviations.

## Reffy References

None. The direction was agreed in the 2026-09-22 discussion that followed the migration: the Python implementation does not need to match JavaScript idiosyncrasies.
