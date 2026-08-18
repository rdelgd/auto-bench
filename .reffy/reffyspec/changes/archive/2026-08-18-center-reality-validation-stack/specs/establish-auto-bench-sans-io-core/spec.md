## MODIFIED Requirements

### Requirement: TypeScript Sans I/O Core
The system SHALL provide a reusable TypeScript library named **Lasm**, with package identity `@lasm/core`, whose LogicalAssembly modeling, agent-facing projection modeling, reality-validation domain modeling, evidence normalization, validation, and deterministic evaluation mechanics remain independent of filesystem, network, process, database, clock, live agent, and live MCP access. Active package metadata, documentation, specifications, workspace identifiers, and examples SHALL identify the library as Lasm rather than Nuveris; archived planning records MAY retain historical Nuveris references.

#### Scenario: Consume Lasm from materialized reality-validation inputs
- **GIVEN** an episode-scoped LogicalAssembly slice, Auto Bench episode, operational state contract, agent-facing projections, and evidence events are materialized as TypeScript values
- **WHEN** a consumer imports and invokes `@lasm/core`
- **THEN** the library returns structured validation and evaluation values that Auto Bench can use to evaluate the Lasm
- **AND** it does not resolve remote assembly entries, read files, call the network, access a database, inspect environment variables, execute an agent, or connect to a live MCP server
- **AND** its active public identity does not introduce a separately named Nuveris middle layer

### Requirement: Scenario Model
The system SHALL model an Auto Bench episode as a serializable fixture containing business context, expected user intent, an episode-scoped LogicalAssembly reference set, expected Lasm projections and control surfaces, initial operational state, actor-relevant observations, permitted or prohibited transitions, acceptable or prohibited outcomes, and evaluation expectations.

#### Scenario: Define an automotive Lasm evaluation episode
- **GIVEN** an Auto Bench episode for an automotive business workflow
- **WHEN** the episode is represented with `@lasm/core`
- **THEN** it identifies the assembly version and entries governing the episode
- **AND** it defines the initial state and the state transitions and outcomes needed to judge success or failure
- **AND** it references the harness, skill, MCP, and authority projections through which the agent encounters or changes that reality
- **AND** it can be validated without an external datastore or runtime integration

### Requirement: Agentic Trace Model
The system SHALL normalize validation evidence for submitted intent, LogicalAssembly selection and consultation, Lasm projections, actor observations, harness behavior, skill usage, MCP usage, policy checks, permissions, human confirmations, handoffs, proposed or committed state transitions, runtime Lasm evaluations, observed outcomes, evidence links, and failure attribution.

#### Scenario: Normalize evidence for evaluating a Lasm
- **GIVEN** evidence events from an Auto Bench episode
- **WHEN** the evidence is normalized
- **THEN** each accepted event has a stable type, position, actor, optional subject, and evidence payload
- **AND** the normalized sequence can distinguish represented reality, projected meaning, observed state, agent inference, proposed action, committed transition, runtime Lasm evaluation, Auto Bench evaluation evidence, and validated outcome
- **AND** malformed or unknown evidence is reported as validation findings rather than causing hidden side effects

### Requirement: Structured Evaluation Results
The system SHALL enable Auto Bench to evaluate a Lasm using structured dimensions for intent fidelity, semantic fidelity, reality-model validity, state and outcome validity, control-surface quality, reality coverage, evidence and attribution, and governance.

#### Scenario: Auto Bench evaluates the Lasm
- **GIVEN** a valid assembly slice, Auto Bench episode, initial state, Lasm projections, and normalized evidence
- **WHEN** the Auto Bench evaluator runs
- **THEN** it returns per-dimension status, findings, and evidence references
- **AND** it can attribute divergence to the reality model, a projection, a control surface, agent conduct, an external system, or insufficient evaluation evidence
- **AND** it treats Lasm runtime evaluation results as evidence rather than equating their passage with conformance of the Lasm as a whole
- **AND** it establishes outcomes from state and evidence rather than an agent's task-completion claim alone

### Requirement: Data Handling Deferral
The system SHALL keep source extraction and reconciliation, persistence, ingestion, transport, UI, generic agent analytics, dashboards, organization-wide telemetry collection, live agent execution, and live integrations outside the `@lasm/core` boundary.

#### Scenario: Integrate external sources and telemetry through adapters
- **GIVEN** an adapter that compiles assembly entries, loads episode state, runs an agent, or imports telemetry from external systems
- **WHEN** the adapter invokes `@lasm/core`
- **THEN** it passes materialized domain values and evidence into the library
- **AND** the library returns materialized validation and evaluation values without taking ownership of sources, storage, transport, collection, orchestration, or analytics presentation

## ADDED Requirements

### Requirement: LogicalAssembly Slice Model
The system SHALL represent an immutable, serializable, episode-scoped LogicalAssembly slice with stable assembly identity, version, provenance, concepts, relations, constraints, events, policies, and runtime evaluation descriptors.

#### Scenario: Validate a materialized assembly slice
- **GIVEN** a materialized assembly slice for an Auto Bench episode
- **WHEN** `@lasm/core` validates the slice
- **THEN** stable entry identifiers and required provenance are checked
- **AND** relations, constraints, policies, runtime evaluations, and projection references resolve to entries in the slice
- **AND** missing, duplicate, or dangling references are returned as addressed validation findings

### Requirement: Lasm Projection Model
The system SHALL represent agent-facing harness, skill, MCP, prompt, permission, approval, and handoff surfaces as projections or controls that MAY reference the LogicalAssembly entries and operational-state contracts they expose or enforce.

#### Scenario: Attribute a lossy agent-facing projection
- **GIVEN** an agent-facing surface references the assembly meaning it projects or enforces
- **WHEN** Auto Bench evidence shows that the surface omitted, distorted, or contradicted that meaning
- **THEN** the evaluator can attribute the divergence to the projection or control surface
- **AND** no separately named middle-layer model is required to connect the surface to the LogicalAssembly

### Requirement: Operational State Transition Model
The system SHALL represent initial operational state, actor-specific observations, proposed and committed transitions, transition constraints, and acceptable or prohibited outcomes as serializable values.

#### Scenario: Validate an episode's resulting state
- **GIVEN** initial state, transition expectations, evidence of actions and committed transitions, and outcome expectations
- **WHEN** Auto Bench evaluates the Lasm episode
- **THEN** the evaluator determines whether observed transitions were permitted
- **AND** it determines whether the resulting state is acceptable or prohibited
- **AND** missing state evidence, delayed effects, side effects, and unresolved outcomes can be reported without relying on a live clock
