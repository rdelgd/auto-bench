# Project Context

## Purpose
SArB is the Servco Automotive Reality Benchmark.

The project exists to model and evaluate how agentic abstractions operate inside realistic automotive business contexts. Its central concern is not every possible use of agents across the organization, but the portion of agentic work that has been successfully codified, modeled, and made evaluable through harnesses, skills, MCP surfaces, policies, traces, and benchmark scenarios.

SArB should help answer:

- Can an agent preserve business intent while moving through harnesses, codified skills, and MCP primitives?
- Are the agent-facing control surfaces legible, scoped, governable, and useful?
- Can realistic automotive workflows be represented well enough to reveal gaps in agent behavior, skill design, MCP exposure, policy boundaries, and operational context?
- Can benchmark traces show where intent was preserved, distorted, expanded, blocked, or successfully completed?

The first implementation direction is a TypeScript Sans I/O core. The core should define the benchmark vocabulary and evaluation behavior before the project commits to a datastore, ingestion pipeline, runtime, UI, deployment target, or analytics product.

## Tech Stack
- TypeScript is the primary implementation language.
- Node.js-compatible tooling is expected for development, tests, and future adapters.
- Markdown and ReffySpec are used for planning, proposals, and project context.
- Harnesses, skills, and MCP are domain concepts to be modeled and evaluated; live MCP integration is not required in the initial core.

## Project Conventions

### Code Style
- Prefer explicit, serializable domain types over loosely shaped objects.
- Keep names domain-driven: scenario, intent, harness, skill, MCP surface, primitive, trace event, evaluation, finding, evidence, policy, handoff, and outcome.
- Use small modules with clear boundaries.
- Prefer deterministic functions that accept materialized values and return materialized values.
- Avoid global state and implicit dependencies in the core.
- Keep comments sparse and useful; explain non-obvious domain decisions rather than restating code.

### Architecture Patterns
- The core is Sans I/O: no filesystem reads, network calls, database access, process environment access, live MCP connections, timers, or runtime orchestration.
- Adapters may load data from files, databases, APIs, event streams, object storage, or live MCP servers, but adapters pass already-materialized values into the core.
- The core owns domain models, validation, trace normalization, and deterministic evaluation.
- Harnesses, skills, and MCP surfaces are modeled as benchmark fixtures before they are treated as live integrations.
- Evaluation should focus on structured results with findings and evidence references, not only a single opaque score.
- Dependency direction should stay inward: UI, CLI, services, storage, and ingestion depend on the core; the core does not depend on them.

### Testing Strategy
- Core behavior should be covered with unit tests for pure validation, trace normalization, and evaluation functions.
- Fixture-level tests should exercise complete benchmark scenarios without filesystem, network, database, clock, or live MCP dependencies inside the core.
- Tests should prefer representative automotive workflow fixtures over abstract toy examples when the domain matters.
- Evaluator tests should assert structured findings and evidence references, not just pass/fail outcomes.
- Any future adapter tests should keep adapter I/O separate from core behavior tests.

### Git Workflow
- No repository-specific branch or commit convention has been established yet.
- Keep changes scoped to the relevant Reffy artifact, ReffySpec change, or implementation task.
- Do not rewrite or discard unrelated user changes.

## Domain Context
SArB treats the agentic abstraction as part of the business reality being benchmarked. The relevant object is not just a final model answer or task result, but the path from user intent through agent role, harness, codified skills, MCP primitives, policy checks, human confirmations, handoffs, and business outcomes.

The benchmark should represent automotive business complexity, including areas such as service, parts, sales, finance, customer experience, inventory, warranty, scheduling, pricing, compliance, and operational policy. Early scenarios should favor workflows where ambiguity, missing context, cross-functional constraints, and governance concerns matter.

Harnesses are treated as agent-hosting or agent-mediating runtime surfaces. Examples include coding and workflow products such as Codex, Claude Code, and OpenCode. A harness frames what the agent can perceive and do through workspace access, context loading, tool permissions, approval flows, transcript shape, invocation modes, and handoff boundaries.

Skills are treated as codified workflow surfaces: reusable instruction and asset bundles that make agent behavior more discoverable, repeatable, controllable, and evaluable.

MCP surfaces are treated as codified system-facing control surfaces: servers and primitives that expose tools, resources, and prompts an agent can discover or use.

Important trace concepts include:

- Submitted user intent.
- Agent role or proxy selected.
- Harness selected, configured, and used.
- Harness context loading, permissions, approval flows, and tool availability.
- Skill discovery and activation.
- Skill references or assets loaded.
- MCP server and primitive discovery.
- MCP tool calls, resource reads, and prompt usage.
- Policy checks and sensitive action gates.
- Human confirmation requests and responses.
- Handoffs between agents, humans, or systems.
- Task success, failure, or partial completion.
- Evidence for intent fidelity and governance quality.

## Important Constraints
- Do not let uncertainty about data handling block the benchmark core.
- Do not bake persistence, transport, ingestion, UI, or analytics collection into core domain logic.
- Do not assume all organizational agent usage is observable or in scope. The initial scope is what can be codified, modeled, and evaluated through harnesses, skills, and MCP.
- Do not require live MCP servers or real agent execution for core tests.
- Preserve a clear distinction between user intent, agent inference, harness behavior, available primitives, selected primitives, policy constraints, and business outcome.
- Treat automotive operational and customer data as potentially sensitive; avoid designing examples that require real customer data unless an explicit privacy model exists.

## External Dependencies
- Agent Skills: a reference point for skill directory structure and skill-based agent control surfaces.
- Model Context Protocol: a reference point for MCP servers, tools, resources, prompts, and agent-facing system integration.
- Agent harnesses: coding and workflow surfaces such as Codex, Claude Code, OpenCode, and future internal harnesses that host or mediate agent behavior.
- Reffy and ReffySpec: repository-local planning, artifact, and proposal workflow.
- Future dependencies for storage, ingestion, telemetry, UI, or live MCP connectivity are intentionally undecided.
