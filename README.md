# Nuveris Core

Nuveris is the agentic control plane through which intent becomes governed capability, action, and evidence. Nuveris Core is its TypeScript Sans I/O implementation: serializable domain models, pure validation, deterministic trace normalization, and structured evaluation without a dependency on storage, transport, runtime orchestration, or live integrations.

Harnesses, codified skills, MCP surfaces, policies, approvals, handoffs, and traces are modeled as agentic control primitives. Core functions accept already-materialized values and return materialized validation or evaluation results.

## Relationship to Auto Bench

Auto Bench is Servco's automotive reference benchmark. It is the first reference benchmark built with Nuveris.

The automotive service-scheduling fixture in `src/fixtures/` demonstrates how Auto Bench can model a realistic workflow with a harness, skill, MCP primitives, policy checks, customer confirmation, trace evidence, and evaluation output.

## Current Status

The repository contains the initial Nuveris Core implementation and its Reffy/ReffySpec planning layer:

- `.reffy/artifacts/agentic-control-primitives-for-auto-bench.md` captures the Nuveris thesis and its relationship to Auto Bench.
- `.reffy/artifacts/naming-the-agentic-control-layer.md` records the Nuveris naming decision.
- `.reffy/reffyspec/specs/establish-auto-bench-sans-io-core/` defines the current core and benchmark contract.
- `src/` contains serializable domain models, validators, trace normalization, and deterministic evaluators.
- `src/fixtures/` contains the Auto Bench automotive service-scheduling reference fixture.

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

## Core Boundary

Filesystem, network, database, environment, clock, persistence, runtime orchestration, and live MCP behavior remain outside Nuveris Core. Future adapters may perform I/O, but they must pass materialized domain values into the core and consume materialized results.
