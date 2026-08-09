# Change: Establish SArB Sans I/O Core

## Why
SArB needs an initial implementation direction that can support benchmarking agentic abstractions without prematurely committing to an application runtime, datastore, ingestion pipeline, UI, or deployment model.

The current thesis is that the strategically relevant surface is not every informal use of agents across the organization. It is the portion of agentic work that becomes codified, modeled, and evaluated through harnesses, skills, and MCP. A Sans I/O TypeScript core gives SArB a stable domain model and evaluation engine for that surface while leaving data handling decisions open.

## What Changes
- Establish TypeScript as the initial implementation language.
- Define a Sans I/O core package that contains pure domain types, validators, state transitions, trace normalization, and evaluators.
- Model SArB scenarios around agentic abstractions that are successfully codified as harnesses, skills, and MCP surfaces.
- Represent harnesses, skills, and MCP primitives as benchmark fixtures without requiring live MCP servers, filesystem reads, network access, or persistent storage inside the core.
- Define trace and evaluation primitives for intent fidelity, control surface quality, business realism, observability, and governance.
- Defer data storage, ingestion, UI, orchestration, live agent execution, and organization-wide analytics products to later changes.

## Impact
- Affected specs: `establish-sarb-sans-io-core`
- Affected code: new TypeScript project/package structure, pure core modules, tests, and fixture examples

## Supersedes
None

## Reffy References
- `agentic-control-primitives-for-sarb.md` - defines the agentic abstraction thesis, harness/skill/MCP control surfaces, candidate benchmark dimensions, and trace markers informing this initial core.
