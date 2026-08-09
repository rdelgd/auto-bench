## Context
Nuveris Core currently evaluates agent use of harnesses, skills, MCP surfaces, policy gates, and task outcomes. That is useful but incomplete: it lacks an explicit semantic substrate, initial and resulting operational state, and a way to attribute divergence between the reality model, its projections, agent conduct, external systems, and evaluation.

## Goals / Non-Goals
- Goals:
  - Make reality validation the organizing responsibility of the stack.
  - Represent the minimum materialized LogicalAssembly slice required by an episode.
  - Represent state observations, transitions, and outcomes explicitly.
  - Produce structured, attributable metaevaluation across the agreed validation dimensions.
  - Preserve deterministic Sans I/O behavior.
- Non-Goals:
  - Extract or reconcile assembly entries from live source systems inside the core.
  - Build a comprehensive organizational ontology or digital twin.
  - Build generic agent analytics, dashboards, funnels, or observability infrastructure.
  - Execute live agents, MCP servers, or runtime Lasm gates inside the core.

## Decisions

### Materialize an episode-scoped LogicalAssembly slice
Benchmark input will carry an immutable, serializable assembly slice with stable identity, version, provenance, and only the concepts, relations, constraints, events, policies, and runtime evaluation descriptors relevant to the episode.

Rationale: deterministic evaluation cannot depend on resolving remote assembly references, while an organization-wide assembly would violate the narrow-waist and minimum-reality scope.

### Model operational state and transitions explicitly
A scenario will describe initial state, actor-relevant observations, permitted or prohibited transitions, and acceptable or prohibited outcomes. Evidence events will record proposed, committed, or rejected transitions and observed outcomes.

Rationale: task completion is a claim; validation requires observable state and transition evidence.

### Treat Nuveris surfaces as projections and consumers
Harness, skill, MCP, and prompt fixtures may reference the assembly entries they project or enforce. The core will validate reference integrity and use those links for attribution.

Rationale: a control surface can be operationally correct yet semantically stale or lossy. Projection references make that distinction testable.

### Keep two evaluation loops distinct
Lasm evaluation descriptors/results represent runtime checks against maintained organizational meaning. Auto Bench metaevaluation judges the whole episode, including the fitness of the reality model and the adequacy of runtime gates.

Rationale: a runtime gate can pass against stale meaning; benchmark success cannot be reduced to gate passage.

### Use validation evidence, not an analytics schema
The event model will include only evidence required to establish reality, conduct, transition, outcome, or attribution. External analytics platforms may consume or augment it.

Rationale: generic activity collection is well served by existing telemetry infrastructure and does not supply organization-specific meaning or judgment.

### Preserve the Sans I/O boundary
The core accepts materialized assemblies, fixtures, states, and evidence and returns materialized validation/evaluation results. Extraction, persistence, clocks, transport, orchestration, dashboards, and live integrations remain adapters.

## Validation Dimensions
- Intent fidelity
- Semantic fidelity
- Reality-model validity
- State and outcome validity
- Control-surface quality
- Reality coverage
- Evidence and attribution
- Governance

## Migration
1. Add LogicalAssembly and operational-state domain models and validators.
2. Extend scenarios and control-surface fixtures with assembly/state references.
3. Expand and rename trace concepts as validation evidence.
4. Replace evaluation dimensions and implement structured findings.
5. Update the automotive fixture and tests as one complete reality-validation episode.

No compatibility alias or legacy fixture adapter is required for the private pre-release package.

## Reffy Inputs
- agentic-control-primitives-for-auto-bench.md

## Open Questions
- What is the smallest useful representation for actor-specific partial observations?
- Should runtime evaluation descriptors include executable identifiers only, or a portable expression subset?
- How should delayed outcomes be represented without introducing a clock into the core?
- Which source-provenance fields are required versus adapter-defined metadata?
