## Context
The shipped package is currently named Nuveris Core and published locally as `@nuveris/core`. It models agent-facing control surfaces and evaluates conformance, but it lacks an explicit semantic substrate, initial and resulting operational state, and a way to attribute divergence between operational reality, its representation, projections, agent conduct, external systems, and evaluation.

The earlier three-layer model treated LogicalAssembly as the semantic substrate, Nuveris as the control layer, and Auto Bench as the evaluator. The revised thesis removes the Nuveris middle layer. A Lasm becomes operational through its projections into harnesses, skills, MCP surfaces, permissions, approvals, and other agent-facing interfaces. Lasm therefore names both the semantic/control thesis and the reusable library; Auto Bench evaluates the Lasm.

## Goals / Non-Goals
- Goals:
  - Use Lasm as the organizing identity for the semantic/domain model and reusable npm library.
  - Remove Nuveris from active architecture and package identity.
  - Make reality validation the organizing responsibility of the stack.
  - Represent the minimum materialized LogicalAssembly slice required by an episode.
  - Represent Lasm projections, state observations, transitions, outcomes, and attributable evidence explicitly.
  - Let Auto Bench produce structured evaluation of the Lasm across the agreed dimensions.
  - Preserve deterministic Sans I/O behavior.
- Non-Goals:
  - Rewrite archived ReffySpec changes that record the former Nuveris decision.
  - Extract or reconcile assembly entries from live source systems inside the core library.
  - Build a comprehensive organizational ontology or digital twin.
  - Build generic agent analytics, dashboards, funnels, or observability infrastructure.
  - Execute live agents, MCP servers, or runtime Lasm gates inside the core library.

## Decisions

### Use Lasm for the thesis, domain model, and library
**Lasm** names the broader thesis and reusable software. **LogicalAssembly** remains the precise name for a materialized domain object composed of concepts, relations, constraints, events, policies, evaluations, provenance, and version identity. The npm package becomes `@lasm/core`.

Rationale: the semantic model and the control surfaces that project and enforce it form one dependency chain. A second proper name creates a boundary the implementation and evidence model must immediately cross.

Public APIs should continue to use precise domain names such as `LogicalAssembly`, `ConformanceCase`, `OperationalState`, and `EvidenceEvent`; the package rename does not justify prefixing every export with `Lasm`.

### Auto Bench evaluates the Lasm
Auto Bench supplies automotive episodes, expectations, fixtures, perturbations, and evidence used to judge a Lasm. Its evaluation asks whether the Lasm was grounded in operational reality, whether projections preserved its meaning and authority, whether the proxy acted conformantly, and whether the resulting state was acceptable.

Rationale: Lasm is the evaluand. Auto Bench is the automotive conformance workbench that exercises it and locates divergence.

The pure evaluation mechanics may be exported by `@lasm/core`, but Auto Bench owns the automotive case and invokes those mechanics to evaluate the Lasm. This keeps the current single-package implementation viable without confusing package location with conceptual responsibility.

### Materialize an episode-scoped LogicalAssembly slice
A conformance case will carry an immutable, serializable assembly slice with stable identity, version, provenance, and only the concepts, relations, constraints, events, policies, and runtime evaluation descriptors relevant to the episode.

Rationale: deterministic evaluation cannot depend on resolving remote assembly references, while an organization-wide assembly would violate the narrow-waist and minimum-reality scope.

### Treat agentic control surfaces as Lasm projections
Harness, skill, MCP, prompt, permission, approval, and handoff fixtures may reference the assembly entries they project or enforce. The library will validate reference integrity and use those links for attribution.

Rationale: a control surface can be operationally correct yet semantically stale or lossy. Projection references make that distinction testable without inventing a separate middle layer.

### Model operational state and transitions explicitly
An Auto Bench episode will describe initial state, actor-relevant observations, permitted or prohibited transitions, and acceptable or prohibited outcomes. Evidence events will record proposed, committed, or rejected transitions and observed outcomes.

Rationale: task completion is a claim; evaluating the Lasm requires observable state and transition evidence.

### Keep two evaluation loops distinct
Lasm runtime evaluation descriptors and results represent checks against maintained organizational meaning. Auto Bench evaluates the Lasm as a whole, including the fitness of the reality model, the fidelity of its projections, and the adequacy of its runtime gates.

Rationale: a runtime gate can pass against stale or incomplete meaning. Auto Bench must treat that result as evidence rather than proof of conformance.

### Use validation evidence, not an analytics schema
The event model will include only evidence required to establish reality, projection, conduct, transition, outcome, or attribution. External analytics platforms may consume or augment it.

Rationale: generic activity collection is well served by existing telemetry infrastructure and does not supply organization-specific meaning or judgment.

### Preserve the Sans I/O boundary
`@lasm/core` accepts materialized assemblies, projections, fixtures, states, and evidence and returns materialized validation and evaluation results. Extraction, persistence, clocks, transport, orchestration, dashboards, and live integrations remain adapter responsibilities.

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
1. Rename the package from `@nuveris/core` to `@lasm/core` and remove active Nuveris identities without changing archived planning records.
2. Add LogicalAssembly and operational-state domain models and validators.
3. Extend scenarios and agent-facing projection fixtures with assembly and state references.
4. Expand trace concepts into Lasm and Auto Bench validation evidence.
5. Replace evaluation dimensions and implement structured findings that evaluate the Lasm.
6. Update the automotive fixture and tests as one complete reality-validation episode.

No compatibility alias or legacy fixture adapter is required for the private pre-release package.

## Reffy Inputs
- `naming-the-agentic-control-layer.md`
- `agentic-control-primitives-for-auto-bench.md`

## Open Questions
- What is the smallest useful representation for actor-specific partial observations?
- Should runtime evaluation descriptors include executable identifiers only, or a portable expression subset?
- How should delayed outcomes be represented without introducing a clock into the core?
- Which source-provenance fields are required versus adapter-defined metadata?
- Which generic evaluation mechanics belong in `@lasm/core`, and which automotive case composition belongs only to Auto Bench?
