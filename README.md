# Auto Bench

Auto Bench is Servco's automotive reference benchmark for validating whether agents perceive, preserve, and act within operational reality—and whether the represented reality remains fit for action.

This repository contains the initial Auto Bench fixture, the reusable Nuveris Core package, and the Reffy/ReffySpec context guiding the stack's evolution.

## The Reality-Validation Stack

| Layer | Responsibility |
| --- | --- |
| **LogicalAssembly (Lasm)** | Defines and continuously tests a scoped, sourced, versioned, and contestable representation of load-bearing operational reality |
| **Nuveris** | Binds agent perception and capability to that reality, governs consequential action, and produces attributable evidence |
| **Auto Bench** | Stress-tests whether that binding holds across realistic automotive episodes |

Operational reality does not mean an exhaustive digital twin or timeless objective truth. It is the smallest set of meanings, states, constraints, authorities, events, and expected outcomes needed to judge a consequential episode.

The stack should answer:

- Was the represented reality current and sufficiently grounded to support action?
- Did the agent preserve intent, meaning, and authority boundaries?
- Did consequential actions produce permitted state transitions?
- Was the resulting business state acceptable, including side effects and delayed effects?
- Can evidence locate divergence in the reality model, a projection, a control surface, agent conduct, an external system, or the evaluator?

## What Exists Today

Nuveris Core is the implemented TypeScript Sans I/O foundation, published locally as `@nuveris/core`. It currently provides:

- Serializable scenario, harness, skill, and MCP fixture models.
- Pure validation and deterministic trace normalization.
- Structured evaluation for intent fidelity, control-surface quality, business realism, observability, and governance.
- An automotive service-scheduling fixture with policy checks, customer confirmation, trace evidence, and evaluation output.

Core functions accept already-materialized values and return materialized validation or evaluation results. They do not perform filesystem, network, database, environment, clock, persistence, runtime orchestration, or live MCP operations.

## Active Direction

The validated but not yet implemented `center-reality-validation-stack` change extends the current core with:

- Episode-scoped LogicalAssembly slices containing concepts, relations, constraints, events, policies, provenance, and runtime evaluation descriptors.
- Explicit initial state, actor observations, permitted or prohibited transitions, and acceptable or prohibited outcomes.
- Validation evidence for assembly use, state change, runtime evaluation, outcome validation, evidence linking, and failure attribution.
- Reality-validation dimensions for semantic fidelity, reality-model validity, state and outcome validity, reality coverage, and evidence attribution.
- A strict distinction between Lasm runtime evaluations and Auto Bench metaevaluation.

The canonical specification continues to describe shipped behavior until that change is implemented and archived.

## Non-Goals

Auto Bench and Nuveris are not intended to:

- Build a general-purpose agent analytics, engagement, funnel, or dashboard product.
- Define a universal taxonomy for every agent interaction.
- Replace telemetry or observability infrastructure supplied by harness vendors and analytics platforms.
- Centralize every organizational data source or construct an omniscient digital twin.

Telemetry is evidence when it supports validation or attribution; collecting activity is not the product thesis.

## Development

```sh
npm install
npm run typecheck
npm test
```

The package exports the core API and reference fixtures separately:

```ts
import { evaluateBenchmark } from "@nuveris/core";
import { routineMaintenanceBenchmark } from "@nuveris/core/fixtures";

const evaluation = evaluateBenchmark(routineMaintenanceBenchmark);
```

## Project Map

- [Reality-validation thesis](.reffy/artifacts/agentic-control-primitives-for-auto-bench.md)
- [Project context](.reffy/reffyspec/project.md)
- [Current canonical specification](.reffy/reffyspec/specs/establish-auto-bench-sans-io-core/spec.md)
- [Active reality-validation change](.reffy/reffyspec/changes/center-reality-validation-stack/proposal.md)
- [Implementation tasks](.reffy/reffyspec/changes/center-reality-validation-stack/tasks.md)
- [Nuveris Core source](src/)
- [Auto Bench automotive fixture](src/fixtures/service-appointment.ts)
