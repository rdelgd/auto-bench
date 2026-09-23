## Context

The Python core was verified against a corpus of outputs recorded from TypeScript. Byte-for-byte parity required three JavaScript emulations. This change removes them without weakening the regression corpus as evidence.

## Decisions

### 1. Python semantics for text and numbers

- Blank means `not value.strip()`, using Python's Unicode whitespace definition.
- Unsequenced events sort after numbered events. Sort key: `(sequence is None, sequence, input index)`.
- Duplicate sequences use Python numeric equality and hashing, so `1 == 1.0`. The message shows the duplicated value with `str()`.
- Integer sequences are values where `isinstance(value, int)` or `float.is_integer()` holds. Requiring `int` would make JSON spelling (`2` vs `2.0`) semantic, which contradicts the version 1 interchange rule that numeric spelling is not semantic.

### 2. Keep the TypeScript record; add reviewed deviations

`tests/corpus/reference/` stays exactly as recorded, so it still reproduces from the TypeScript revision. `tests/corpus/deviations.json` maps a case ID to a `reason` and JSON Patch operations on that case's expected value. The harness applies the patches, and the parity test compares against the result. Tests reject deviations for unknown cases, deviations without a reason, and no-op deviations. This keeps every difference from the historical reference visible and explained, instead of regenerating expected outputs.

### 3. Unchanged

- The interchange safe-integer bound (±9007199254740991). It is a deliberate wire rule that keeps integers exact for any JSON consumer, not an emulation.
- Message templates, codes, paths, and all evaluation semantics.

## Alternatives considered

- **Edit the recorded corpus in place.** This is simpler, but the corpus would no longer reproduce from the recorded TypeScript revision, and the differences would be hidden in history.
- **Require `int` sequences.** This is stricter, but it makes `2.0` invalid even though JSON considers it the same number as `2`.
