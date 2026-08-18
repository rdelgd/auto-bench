## 1. Planning
- [x] 1.1 Review the conformance-first artifact, canonical spec, active changes, implementation, and tests.
- [x] 1.2 Define the breaking public-symbol and evaluation-dimension migration.
- [x] 1.3 Validate the refined change before implementation.

## 2. Public API And Fixtures
- [x] 2.1 Rename the public input, output, and evaluator to `ConformanceCase`, `ConformanceEvaluation`, and `evaluateConformance`.
- [x] 2.2 Rename the routine-maintenance fixture to `routineMaintenanceConformanceCase`.
- [x] 2.3 Rename `business-realism` and its finding codes to operational-grounding terminology.
- [x] 2.4 Remove old benchmark-oriented code exports without compatibility aliases.

## 3. Tests And Documentation
- [x] 3.1 Update tests for the renamed API, fixture, dimension, and finding codes.
- [x] 3.2 Update package metadata and README examples to describe the shipped conformance API.
- [x] 3.3 Update project context and the active reality-validation change to build on conformance terminology.

## 4. Verification
- [x] 4.1 Confirm no benchmark-oriented identifiers remain in shipped source, tests, or package metadata.
- [x] 4.2 Run typecheck, build, and the full test suite.
- [x] 4.3 Validate and review `adopt-conformance-api`.
- [x] 4.4 Archive the change only after implementation is complete and canonical specs can be updated truthfully.
