## Context
SArB is being framed as the Servco Automotive Reality Benchmark: a way to evaluate how agentic abstractions operate within realistic automotive business contexts. The initial implementation should avoid entangling the core benchmark model with data handling, app runtime, live integrations, or persistence. The core should be usable from tests, CLIs, services, notebooks, or future UIs without changing its behavior.

### Problem Summary
Agentic abstractions are expected to be distributed across the organization, but SArB should not attempt to observe every informal agent interaction at first. The initial scope is the subset of agentic work that is successfully codified, modeled, and evaluable through harnesses, skills, and MCP primitives.

That scope needs a stable way to describe:

- A business scenario and its expected intent.
- The harness mediating agent operation, context, tools, permissions, approvals, and interaction loop.
- The codified skills available to an agent.
- The MCP servers and primitives exposed to the agent.
- The trace of agentic events produced while attempting the scenario.
- Evaluation results that explain whether the trace preserved intent, used the right control surfaces, and respected governance expectations.

## Goals / Non-Goals
Goals:

- Implement the first SArB core in TypeScript.
- Keep core modules Sans I/O: deterministic, side-effect free, and independent of filesystem, network, clocks, databases, environment variables, and process globals.
- Define serializable domain types for scenarios, harnesses, skills, MCP surfaces, trace events, and evaluations.
- Support fixture-driven tests so benchmark behavior can be developed before the data layer is known.
- Make harnesses, skills, and MCP first-class control primitives in the benchmark model.
- Provide enough validation to reject malformed fixtures and traces at core boundaries.

Non-Goals:

- Do not implement a datastore, ingestion pipeline, API server, UI, or dashboard.
- Do not connect to live MCP servers in the core.
- Do not execute real agent runs in the core.
- Do not define organization-wide analytics collection or telemetry transport.
- Do not require a final data warehouse, event bus, or schema registry decision.

## Decisions
Decision: Use TypeScript for the first implementation.

Rationale: TypeScript gives SArB typed domain models, straightforward JSON fixture handling, and compatibility with likely agent tooling, MCP clients, CLIs, and web-facing evaluation surfaces.

Decision: Keep the core Sans I/O.

Rationale: SArB's early uncertainty is mostly about data handling and runtime integration. A pure core lets the project progress on the benchmark vocabulary, validators, and evaluators while adapters for storage, ingestion, live MCP, or UI are deferred.

Decision: Treat harnesses, skills, and MCP as benchmark fixtures, not live integrations.

Rationale: The relevant benchmark space is what has been codified and can be modeled. A fixture can describe a harness, skill, MCP server, tool, resource, prompt, or policy boundary without requiring the core to discover or invoke it directly.

Decision: Evaluate traces rather than opaque final answers only.

Rationale: The SArB thesis depends on whether intent moved through the agentic abstraction in a legible and governable way. Final task outcome matters, but the trace is where harness behavior, skill activation, MCP selection, policy checks, handoffs, and intent preservation become measurable.

Decision: Represent unknown data handling through ports outside the core.

Rationale: Future adapters can load scenarios, traces, and fixtures from files, databases, APIs, object storage, or MCP servers. The core should only accept already-materialized data structures and return data structures.

## Proposed Module Shape

The first implementation should prefer a small package with modules similar to:

- `domain`: shared branded ids, result types, and serializable records.
- `scenario`: benchmark scenario definitions and expected intent.
- `harness`: harness descriptors for agent-hosting runtime surfaces, permissions, context, and approvals.
- `skill`: codified skill descriptors and workflow capabilities.
- `mcp`: MCP server and primitive descriptors for tools, resources, and prompts.
- `trace`: normalized agentic event model.
- `evaluate`: deterministic evaluators and score/explanation outputs.
- `validate`: fixture and trace validation helpers.

Exact filenames can change during implementation, but the dependency direction should stay inward: adapters can depend on the core, while the core depends on no adapter.

## Evaluation Model

The initial evaluator should produce structured output rather than a single opaque score. Candidate dimensions:

- Intent fidelity: whether explicit user intent and expected business goal are preserved.
- Control surface quality: whether harness affordances, skills, and MCP primitives are relevant, scoped, and correctly selected.
- Business realism: whether required automotive context is represented in the scenario and trace.
- Observability: whether an evaluator can reconstruct what happened and why.
- Governance: whether permissions, policy checks, sensitive actions, and human confirmations are represented.

Each dimension can start as a rule-based evaluator that returns status, findings, and evidence references. Numeric scoring can be added later after the domain vocabulary stabilizes.

## Reffy Inputs
- agentic-control-primitives-for-sarb.md

## Open Questions
- Which automotive workflows should become the first canonical scenarios?
- Should fixture schemas be hand-authored TypeScript validators, generated JSON Schema, or both?
- Should evaluations return only structured findings initially, or also provisional numeric scores?
- What minimum harness metadata is required before an evaluator can judge context, permissions, approvals, and tool availability?
- What minimum MCP primitive metadata is required before an evaluator can judge control surface quality?
- How much of a skill directory should be modeled initially: metadata only, `SKILL.md` content, supporting references, scripts, or all declared assets?
