# Project Context

## Purpose
The Auto Bench–Nuveris–Lasm stack is a reality-validation system. It should determine whether agents perceive, preserve, and act within an organization's operational reality, whether the represented reality remains fit for action, what state changed, and where correction is needed.

- A **LogicalAssembly (Lasm)** defines and continuously tests a scoped, sourced, versioned, and contestable representation of load-bearing operational reality.
- **Nuveris** binds agent perception and capability to that reality, governs consequential action through agent-facing control surfaces, and produces attributable evidence.
- **Auto Bench** stress-tests whether that binding holds across realistic automotive episodes.

Operational reality is not an exhaustive digital twin or a claim to timeless objective truth. It is the smallest set of meanings, states, constraints, authorities, events, and expected outcomes needed to judge a consequential episode.

The stack should help answer:

- Was the represented reality current and sufficiently grounded to support action?
- Did the agent preserve intent and organizational meaning across projections, harnesses, skills, MCP primitives, policies, approvals, and handoffs?
- Did consequential actions respect authority and produce permitted state transitions?
- Was the resulting business state acceptable, including delayed effects and side effects?
- Can evidence locate divergence in the reality model, a projection, a control surface, agent conduct, an external system, or the evaluator?

The first implementation direction remains Nuveris Core, published locally as `@nuveris/core`. It should provide the reusable TypeScript Sans I/O vocabulary and deterministic validation/evaluation behavior for materialized Lasm slices, Nuveris control surfaces, Auto Bench episodes, state transitions, outcomes, and evidence before the project commits to a datastore, ingestion pipeline, runtime, UI, deployment target, or analytics product.

## Tech Stack
- TypeScript is the primary implementation language.
- The core package identity is `@nuveris/core`.
- Node.js-compatible tooling is expected for development, tests, and future adapters.
- Markdown and ReffySpec are used for planning, proposals, and project context.
- Logical Assemblies, harnesses, skills, MCP surfaces, operational state, transitions, outcomes, and evidence are domain concepts to be modeled and evaluated.
- Live MCP integration, live agent execution, and source-system ingestion are not required in the initial core.

## Project Conventions

### Code Style
- Prefer explicit, serializable domain types over loosely shaped objects.
- Keep names domain-driven: LogicalAssembly, concept, relation, constraint, event, policy, projection, operational state, state transition, scenario, intent, harness, skill, MCP surface, evidence event, evaluation, finding, handoff, and outcome.
- Use small modules with clear boundaries.
- Prefer deterministic functions that accept materialized values and return materialized values.
- Avoid global state and implicit dependencies in the core.
- Keep comments sparse and useful; explain non-obvious domain decisions rather than restating code.

### Architecture Patterns
- The core is Sans I/O: no filesystem reads, network calls, database access, process environment access, live MCP connections, timers, or runtime orchestration.
- Adapters may load data from files, databases, APIs, event streams, object storage, or live MCP servers, but adapters pass already-materialized values into the core.
- The core owns domain models, validation, evidence normalization, deterministic Lasm evaluation inputs/results, and deterministic Auto Bench metaevaluation.
- Materialized LogicalAssembly slices are runtime-independent inputs; source extraction and reconciliation remain adapter concerns.
- Harnesses, skills, MCP surfaces, and prompts are modeled as projections or consumers of assembly meaning before they are treated as live integrations.
- Operational state and transitions are explicit benchmark objects rather than facts inferred only from task-completion claims.
- Lasm evaluations gate or check behavior against maintained meaning; Auto Bench evaluations judge the assembled episode. Keep these roles distinct even when runtime evaluation results become benchmark evidence.
- Evaluation should focus on structured results with findings and evidence references, not only a single opaque score.
- Dependency direction should stay inward: UI, CLI, services, storage, and ingestion depend on the core; the core does not depend on them.

### Testing Strategy
- Core behavior should be covered with unit tests for pure validation, trace normalization, and evaluation functions.
- Fixture-level tests should exercise complete benchmark scenarios without filesystem, network, database, clock, or live MCP dependencies inside the core.
- Tests should prefer representative automotive workflow fixtures over abstract toy examples when the domain matters.
- Tests should cover stale or incoherent assembly entries, lossy projections, incorrect initial-state observations, prohibited transitions, unacceptable outcomes, delayed effects, and insufficient attribution evidence.
- Evaluator tests should assert structured findings, addressed semantic entries, state transitions, and evidence references, not just pass/fail outcomes.
- Replacement tests should demonstrate that critical meaning and validation survive a change of model, harness, skill projection, or application representation where practical.
- Any future adapter tests should keep adapter I/O separate from core behavior tests.

### Git Workflow
- No repository-specific branch or commit convention has been established yet.
- Keep changes scoped to the relevant Reffy artifact, ReffySpec change, or implementation task.
- Do not rewrite or discard unrelated user changes.

## Domain Context
The relevant benchmark object is the evidence chain between represented operational reality, agent conduct, and resulting operational reality. A task-completion claim is insufficient without evidence of the governing meaning, observed state, authority, action, transition, and outcome.

A LogicalAssembly slice contains the concepts, relations, constraints, events, policies, and runtime evaluations needed by an episode. It is compiled and reconciled from already load-bearing sources such as schemas, code, policy documents, and observed practice. The core consumes the materialized slice; it does not own extraction or claim to model the whole organization.

Nuveris treats the agentic control plane as the layer that projects, exposes, constrains, and observes agent capability against that assembly. Skills may encode workflows over assembly meaning, MCP primitives may expose typed actions and resources, and harnesses may enforce assembly-derived permissions and approvals.

Auto Bench applies that stack to automotive business complexity, including service, parts, sales, finance, customer experience, inventory, warranty, scheduling, pricing, compliance, and operational policy. Early scenarios should favor workflows where ambiguity, missing context, source disagreement, changing state, cross-functional constraints, governance, and delayed outcomes matter.

Harnesses are treated as agent-hosting or agent-mediating runtime surfaces. Examples include coding and workflow products such as Codex, Claude Code, and OpenCode. A harness frames what the agent can perceive and do through workspace access, context loading, tool permissions, approval flows, transcript shape, invocation modes, and handoff boundaries.

Skills are treated as codified workflow surfaces: reusable instruction and asset bundles that make agent behavior more discoverable, repeatable, controllable, and evaluable.

MCP surfaces are treated as codified system-facing control surfaces: servers and primitives that expose tools, resources, and prompts an agent can discover or use.

Important validation-evidence concepts include:

- Submitted user intent.
- LogicalAssembly identity, version, provenance, and relevant entry references.
- Assembly projections loaded or consulted by agent-facing surfaces.
- Initial operational state and actor-specific observations.
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
- Proposed, committed, and rejected state transitions.
- Runtime Lasm evaluation requests, results, and addressed entries.
- Observed and validated outcomes, including side effects or delayed effects.
- Linked evidence for intent fidelity, semantic fidelity, reality-model validity, state and outcome validity, control-surface quality, reality coverage, attribution, and governance.

## Important Constraints
- Use Nuveris for the reusable core and Auto Bench for Servco's automotive reference benchmark; do not conflate their identities.
- Treat Lasm, Nuveris, and Auto Bench as complementary layers; do not collapse runtime semantic enforcement into benchmark metaevaluation.
- Keep operational reality scoped, sourced, versioned, and capable of representing disagreement.
- Do not let uncertainty about data handling block the benchmark core.
- Do not bake persistence, transport, ingestion, UI, or analytics collection into core domain logic.
- Do not build a general-purpose agent analytics, engagement, funnel, or dashboard product.
- Do not define a universal event taxonomy, centralize every organizational data source, or construct an omniscient digital twin.
- Collect evidence because it supports validation or attribution, not merely because activity is measurable.
- Do not assume all organizational agent usage is observable or in scope. The initial scope is what can be codified, modeled, and evaluated through harnesses, skills, and MCP.
- Do not require live MCP servers or real agent execution for core tests.
- Preserve a clear distinction between user intent, agent inference, harness behavior, available primitives, selected primitives, policy constraints, and business outcome.
- Preserve a clear distinction between represented reality, observed state, agent inference, proposed action, committed transition, runtime evaluation, benchmark evaluation, and validated outcome.
- Treat automotive operational and customer data as potentially sensitive; avoid designing examples that require real customer data unless an explicit privacy model exists.

## External Dependencies
- Durable Forms and Logical Assemblies: the conceptual basis for runtime-independent, evaluation-reachable organizational meaning and consumer-specific projections.
- Agent Skills: a reference point for skill directory structure and skill-based agent control surfaces.
- Model Context Protocol: a reference point for MCP servers, tools, resources, prompts, and agent-facing system integration.
- Agent harnesses: coding and workflow surfaces such as Codex, Claude Code, OpenCode, and future internal harnesses that host or mediate agent behavior.
- Reffy and ReffySpec: repository-local planning, artifact, and proposal workflow.
- Future dependencies for storage, ingestion, telemetry, UI, or live MCP connectivity are intentionally undecided.
