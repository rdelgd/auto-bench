# SArB

SArB is the Servco Automotive Reality Benchmark.

The project is exploring how to model and evaluate agentic abstractions inside realistic automotive business contexts. Its initial focus is the portion of agentic work that can be codified, modeled, and evaluated through harnesses, skills, MCP surfaces, policies, traces, and benchmark scenarios.

The current implementation direction is a TypeScript Sans I/O core: pure domain models, validation, trace normalization, and evaluation logic before committing to a datastore, ingestion pipeline, runtime, UI, or analytics product.

## Current Status

This repository currently contains the Reffy and ReffySpec planning layer for the project:

- `.reffy/artifacts/agentic-control-primitives-for-sarb.md` captures the early thesis.
- `.reffy/reffyspec/project.md` defines the project context.
- `.reffy/reffyspec/changes/establish-sarb-sans-io-core/` contains the active proposal for the initial TypeScript Sans I/O core.

## Development Direction

The first implementation should model:

- Harnesses that mediate agent operation, context, permissions, and approvals.
- Skills as codified workflow surfaces.
- MCP servers and primitives as agent-facing system surfaces.
- Agentic traces that show how intent moves through the system.
- Structured evaluations for intent fidelity, control surface quality, business realism, observability, and governance.
