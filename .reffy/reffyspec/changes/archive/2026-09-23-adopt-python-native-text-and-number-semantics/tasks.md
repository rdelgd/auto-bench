## 1. Implementation

- [x] 1.1 Replace JavaScript whitespace trimming with `str.strip()` for required strings and trace actors; remove `lasm_core._js`.
- [x] 1.2 Sort unsequenced trace events after all numbered events, keeping input order for ties.
- [x] 1.3 Compare duplicate sequences numerically and report them with Python number spelling; keep integer-valued floats valid.

## 2. Regression Corpus

- [x] 2.1 Add `tests/corpus/deviations.json` with a reason and JSON Patch for each intentionally changed reference case; leave `tests/corpus/reference/` unedited.
- [x] 2.2 Apply deviations in the corpus harness, and reject unknown, unexplained, or no-op deviations.
- [x] 2.3 Add direct tests for Python whitespace, numeric sequence equality, and unsequenced ordering.

## 3. Verification and Documentation

- [x] 3.1 Run tests and strict typing on Python 3.11 and 3.13.
- [x] 3.2 Update corpus provenance and verification notes, the migration guide, the API inventory, and the project context.
- [x] 3.3 Run `reffy plan validate adopt-python-native-text-and-number-semantics` and `reffy validate`, then archive the change.
