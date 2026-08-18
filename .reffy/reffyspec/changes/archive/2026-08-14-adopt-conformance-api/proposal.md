# Change: Adopt Conformance API

## Why
Nuveris Core still exposes the public symbols `BenchmarkInput`, `BenchmarkEvaluation`, and `evaluateBenchmark`, and its reference fixture is named `routineMaintenanceBenchmark`. Those names encode the earlier idea that competitive benchmarking is the core product.

The conformance-first direction gives the core a different responsibility: model a materialized conformance case and return structured findings about whether agentic conduct remained faithful to the supplied scenario, control surfaces, operational context, and governance expectations. Auto Bench may later distill a public benchmark from mature conformance cases, but benchmark terminology should not define the reusable core API.

The package is private and pre-release, so this is the right time for a clean breaking rename rather than a compatibility layer.

## What Changes
- Rename `BenchmarkInput` to `ConformanceCase`.
- Rename `BenchmarkEvaluation` to `ConformanceEvaluation`.
- Rename `evaluateBenchmark` to `evaluateConformance`.
- Rename the reference fixture `routineMaintenanceBenchmark` to `routineMaintenanceConformanceCase`.
- Rename the `business-realism` dimension to `operational-grounding` and its `business.*` finding codes to `operational.*`.
- Update tests, package metadata, README examples, project context, and active ReffySpec planning language to use conformance terminology.
- Preserve the current Sans I/O behavior and evaluation logic except for the explicit dimension and finding-code rename.

## Impact
- Affected specs: `establish-auto-bench-sans-io-core`
- Affected code: `src/evaluate.ts`, `src/fixtures/service-appointment.ts`, tests, package metadata, README, project context, and the active `center-reality-validation-stack` change
- Compatibility: the old benchmark-oriented exports and fixture name are removed without aliases; consumers must migrate to the new names

## Relationship To Active Work
This change is a terminology and API foundation for `center-reality-validation-stack`. It does not supersede that change or implement its LogicalAssembly, operational-state, transition, outcome, or expanded evidence models. The active change will be updated to build on the conformance API rather than reintroduce benchmark-oriented core vocabulary.

## Reffy References
- `operational-conformance-first-benchmark-second.md` - establishes operational conformance as the primary purpose and a shareable benchmark as a downstream distillation
