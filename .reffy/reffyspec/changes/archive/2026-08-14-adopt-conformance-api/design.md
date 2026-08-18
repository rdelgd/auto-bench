## Context
The shipped Nuveris Core implementation is small and deterministic, but its main input, output, evaluator, and reference fixture retain benchmark-oriented names. The new project thesis treats Auto Bench as a conformance workbench and Nuveris Core as the runner-neutral vocabulary and evaluator used by that workbench.

This change aligns the public surface without prematurely implementing the larger reality-validation model already planned in `center-reality-validation-stack`.

## Goals / Non-Goals

### Goals
- Make conformance the explicit identity of the public evaluation API.
- Use `ConformanceCase` for the complete materialized input to an evaluation.
- Preserve deterministic Sans I/O behavior.
- Make the current operational-context dimension describe grounding rather than simulated “realism.”
- Leave active future planning consistent with the renamed API.

### Non-Goals
- Add LogicalAssembly, provenance, state-transition, outcome-envelope, or expanded evidence models.
- Rename the general `Scenario`, `EvaluationDimension`, `DimensionResult`, or `EvaluationFinding` types.
- Change evaluation algorithms beyond the named dimension and finding-code migration.
- Add deprecation aliases or an adapter for the old private API.
- Implement a public benchmark or execution harness.

## Decisions

### Use a case noun for the materialized input

| Previous symbol | New symbol |
| --- | --- |
| `BenchmarkInput` | `ConformanceCase` |
| `BenchmarkEvaluation` | `ConformanceEvaluation` |
| `evaluateBenchmark` | `evaluateConformance` |
| `routineMaintenanceBenchmark` | `routineMaintenanceConformanceCase` |

`ConformanceCase` describes a stable evaluative object rather than the mechanics of a function argument. It can later grow to include the Lasm slice, operational state, transition expectations, outcomes, and evidence required by the active reality-validation change.

### Make a clean break
No compatibility exports will be retained. The package is private, at version 0.1.0, and has a small in-repository consumer surface. Aliases would keep the discarded product framing alive and create two names for the same concept before external compatibility matters.

### Rename realism to grounding
`business-realism` implies that the evaluator judges whether a simulation resembles business. The current implementation actually checks whether required operational facts are evidenced. The dimension becomes `operational-grounding`, and finding codes move from `business.*` to `operational.*`.

The predicate itself does not change in this refactor. The active reality-validation change will later replace or expand dimensions using explicit Lasm and operational-state evidence.

### Keep Auto Bench and Nuveris distinct
Auto Bench remains the automotive conformance workbench and potential source of a derived benchmark. Nuveris Core remains the reusable, runner-neutral Sans I/O package. Removing benchmark terminology from Nuveris Core does not remove Auto Bench's identity or prevent later benchmark distribution.

### Update active planning in place
`center-reality-validation-stack` is active, not archived. Its proposal, design, tasks, and delta spec will be edited to use the conformance API and conformance evaluation vocabulary so its later implementation does not reverse this change.

## Migration

```ts
// Before
import { evaluateBenchmark, type BenchmarkInput } from "@nuveris/core";

// After
import { evaluateConformance, type ConformanceCase } from "@nuveris/core";
```

Consumers must also replace `routineMaintenanceBenchmark` with `routineMaintenanceConformanceCase`, expect `operational-grounding` instead of `business-realism`, and update any matching finding codes from `business.*` to `operational.*`.

## Reffy Inputs
- `operational-conformance-first-benchmark-second.md`

## Open Questions
- Should the later reality-validation implementation rename `Scenario` to `Episode`, or should a conformance case continue to contain a general scenario? This is deferred because neither name encodes the discarded benchmark-first framing.
