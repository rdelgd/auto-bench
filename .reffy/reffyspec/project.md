# Project Context

## Purpose
The Lasm–Auto Bench stack is an operational-conformance and reality-validation system. It should determine whether agents perceive, preserve, and act within an organization's operational reality, whether the represented reality remains fit for action, what state changed, and where correction is needed.

- **Lasm** is the thesis, semantic/domain model, and reusable library. A LogicalAssembly defines and continuously tests a scoped, sourced, versioned, and contestable representation of load-bearing operational reality. Its projections expose and enforce that meaning through agent-facing surfaces.
- **Auto Bench** is the automotive conformance workbench that exercises and evaluates the Lasm across realistic episodes.

Servco's lived operations are the initial source reference. A portable automotive benchmark may later be distilled from mature conformance cases, but it is a downstream export rather than the reason for the stack.

Operational reality is not an exhaustive digital twin or timeless objective truth. It is the smallest set of meanings, states, constraints, authorities, events, and expected outcomes needed to judge a consequential episode.

The stack should answer:

- Was the represented reality current and sufficiently grounded to support action?
- Did Lasm projections preserve intent and organizational meaning across harnesses, skills, MCP primitives, policies, approvals, and handoffs?
- Did consequential actions respect authority and produce permitted state transitions?
- Was the resulting business state acceptable, including delayed effects and side effects?
- Can evidence locate divergence in the reality model, a projection, a control surface, agent conduct, an external system, or the evaluator?

The reusable implementation is `@lasm/core`. It provides TypeScript Sans I/O vocabulary and deterministic validation and evaluation mechanics for materialized LogicalAssembly slices, projections, Auto Bench episodes, state transitions, outcomes, and evidence.

## Tech Stack
- TypeScript is the primary implementation language.
- The package identity is `@lasm/core`.
- Node.js-compatible tooling is used for development and tests.
- Markdown and ReffySpec are used for planning and project context.
- Live MCP integration, live agent execution, source-system ingestion, persistence, and UI are adapter concerns.

## Project Conventions

### Code Style
- Prefer explicit, serializable domain types over loosely shaped objects.
- Keep names domain-driven: LogicalAssembly, concept, relation, constraint, event, policy, projection, operational state, state transition, scenario, intent, harness, skill, MCP surface, evidence event, evaluation, finding, handoff, and outcome.
- Use small modules with clear boundaries.
- Prefer deterministic functions that accept materialized values and return materialized values.
- Avoid global state and implicit dependencies in the core library.

### Architecture Patterns
- The library is Sans I/O: no filesystem reads, network calls, database access, process environment access, live MCP connections, timers, or runtime orchestration.
- Adapters pass already-materialized values into the library.
- The library owns domain models, cross-reference validation, evidence normalization, runtime-evaluation records, and deterministic evaluation mechanics.
- Materialized LogicalAssembly slices are runtime-independent inputs; source extraction and reconciliation remain adapter concerns.
- Harnesses, skills, MCP surfaces, prompts, permissions, approvals, and handoffs are Lasm projections or controls that may reference assembly entries and operational-state fields.
- Operational state and transitions are explicit conformance objects rather than facts inferred from task-completion claims.
- Lasm runtime evaluations gate or check behavior against maintained meaning; Auto Bench evaluates the Lasm as a whole.
- Evaluation produces structured findings with evidence, assembly-entry, transition, outcome, and attribution references.
- Dependency direction stays inward: UI, CLI, services, storage, ingestion, and runners depend on the library; the library does not depend on them.

### Testing Strategy
- Core behavior is covered with unit tests for validation, evidence normalization, and evaluation functions.
- Fixture tests exercise complete conformance cases without filesystem, network, database, clock, or live MCP dependencies.
- Tests prefer representative automotive workflows where domain meaning matters.
- Tests cover stale or incoherent assembly entries, lossy projections, incorrect state references, prohibited transitions, unacceptable outcomes, and insufficient attribution evidence.
- Evaluator tests assert structured findings and addressed semantic entries, transitions, outcomes, evidence, and attribution.

### Git Workflow
- No repository-specific branch or commit convention has been established.
- Keep changes scoped to the relevant Reffy artifact, ReffySpec change, or implementation task.
- Do not rewrite or discard unrelated user changes.

## Domain Context
A `ConformanceCase` is the materialized evidence chain between represented operational reality, agent conduct, and resulting operational reality. It contains:

- an episode-scoped LogicalAssembly and provenance;
- initial operational state and actor-specific observations;
- permitted or prohibited transitions and acceptable or prohibited outcomes;
- Lasm projections through harness, skill, MCP, permission, approval, and handoff fixtures;
- normalized evidence for intent, assembly selection and consultation, projections, state, runtime evaluation, actions, outcomes, links, and attribution.

A LogicalAssembly contains concepts, relations, constraints, events, policies, and runtime evaluations. It is compiled from already load-bearing sources such as schemas, code, policy documents, observed practice, incidents, commitments, and practitioner judgment. Each entry identifies its provenance.

Auto Bench evaluates the Lasm across intent fidelity, semantic fidelity, reality-model validity, state and outcome validity, control-surface quality, reality coverage, evidence and attribution, and governance.

## Important Constraints
- Use Lasm for the thesis, semantic model, and reusable package; use Auto Bench for the automotive evaluator.
- Preserve the distinction between a LogicalAssembly domain object, the broader Lasm identity, and Auto Bench evaluation.
- Keep operational reality scoped, sourced, versioned, and capable of representing disagreement.
- Do not bake persistence, transport, ingestion, UI, analytics collection, or live orchestration into core domain logic.
- Do not build a general-purpose agent analytics, engagement, funnel, or dashboard product.
- Collect evidence because it supports validation or attribution, not merely because activity is measurable.
- Preserve distinctions among represented reality, projected meaning, observed state, agent inference, proposed action, committed transition, runtime evaluation, Auto Bench evaluation, and validated outcome.
- Treat automotive operational and customer data as potentially sensitive.

## External Dependencies
- Durable Forms and Logical Assemblies provide the conceptual basis for runtime-independent, evaluation-reachable organizational meaning and consumer-specific projections.
- Agent Skills provide a reference for skill-based agent control surfaces.
- Model Context Protocol provides a reference for tools, resources, prompts, and agent-facing system integration.
- Agent harnesses such as Codex, Claude Code, and OpenCode illustrate runtimes that host or mediate agent behavior.
- Reffy and ReffySpec provide repository-local artifact and planning workflows.
