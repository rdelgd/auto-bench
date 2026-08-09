## MODIFIED Requirements

### Requirement: TypeScript Sans I/O Core
The system SHALL provide a TypeScript core named **Nuveris Core**, with package identity `@nuveris/core`, whose LogicalAssembly modeling, reality-validation domain modeling, evidence normalization, validation, and metaevaluation behavior remain deterministic and independent of filesystem, network, process, database, clock, live agent, and live MCP access.

#### Scenario: Consume Nuveris Core from materialized reality-validation inputs
- **GIVEN** an episode-scoped LogicalAssembly slice, benchmark scenario, operational state contract, control-surface fixtures, and evidence events are materialized as TypeScript values
- **WHEN** a consumer imports and invokes `@nuveris/core`
- **THEN** the core returns structured validation and evaluation results
- **AND** it does not resolve remote assembly entries, read files, call the network, access a database, inspect environment variables, execute an agent, or connect to a live MCP server

### Requirement: Scenario Model
The system SHALL model an Auto Bench episode as a serializable fixture containing business context, expected user intent, an episode-scoped LogicalAssembly reference set, expected agentic control surfaces, initial operational state, actor-relevant observations, permitted or prohibited transitions, acceptable or prohibited outcomes, and evaluation expectations.

#### Scenario: Define an automotive reality-validation episode
- **GIVEN** an Auto Bench episode for an automotive business workflow
- **WHEN** the episode is represented with Nuveris Core
- **THEN** it identifies the assembly version and entries governing the episode
- **AND** it defines the initial state and the state transitions and outcomes needed to judge success or failure
- **AND** it references the harness, skill, and MCP projections through which the agent encounters or changes that reality
- **AND** it can be validated without an external datastore or runtime integration

### Requirement: Agentic Trace Model
The system SHALL normalize validation evidence for submitted intent, LogicalAssembly selection and consultation, projections, actor observations, harness behavior, skill usage, MCP usage, policy checks, permissions, human confirmations, handoffs, proposed or committed state transitions, runtime Lasm evaluations, observed outcomes, evidence links, and failure attribution.

#### Scenario: Normalize reality-validation evidence
- **GIVEN** evidence events from an Auto Bench episode
- **WHEN** the evidence is normalized
- **THEN** each accepted event has a stable type, position, actor, optional subject, and evidence payload
- **AND** the normalized sequence can distinguish represented reality, observed state, agent inference, proposed action, committed transition, runtime evaluation, benchmark evaluation evidence, and validated outcome
- **AND** malformed or unknown evidence is reported as validation findings rather than causing hidden side effects

### Requirement: Structured Evaluation Results
The system SHALL metaevaluate an Auto Bench episode using structured dimensions for intent fidelity, semantic fidelity, reality-model validity, state and outcome validity, control-surface quality, reality coverage, evidence and attribution, and governance.

#### Scenario: Evaluate a reality-validation episode
- **GIVEN** a valid assembly slice, scenario, initial state, control-surface projections, and normalized evidence
- **WHEN** the Auto Bench evaluator runs
- **THEN** it returns per-dimension status, findings, and evidence references
- **AND** it can attribute divergence to the reality model, a projection, a control surface, agent conduct, an external system, or insufficient evaluation evidence
- **AND** it treats Lasm runtime evaluation results as evidence rather than equating their passage with benchmark success
- **AND** it establishes outcomes from state and evidence rather than an agent's task-completion claim alone

### Requirement: Data Handling Deferral
The system SHALL keep source extraction and reconciliation, persistence, ingestion, transport, UI, generic agent analytics, dashboards, organization-wide telemetry collection, live agent execution, and live integrations outside the core boundary.

#### Scenario: Integrate external sources and telemetry through adapters
- **GIVEN** an adapter that compiles assembly entries, loads episode state, or imports telemetry from external systems
- **WHEN** the adapter invokes the core
- **THEN** it passes materialized domain values and evidence into the core
- **AND** the core returns materialized validation and evaluation values without taking ownership of sources, storage, transport, collection, orchestration, or analytics presentation

## ADDED Requirements

### Requirement: LogicalAssembly Slice Model
The system SHALL represent an immutable, serializable, episode-scoped LogicalAssembly slice with stable assembly identity, version, provenance, concepts, relations, constraints, events, policies, and runtime evaluation descriptors.

#### Scenario: Validate a materialized assembly slice
- **GIVEN** a materialized assembly slice for an Auto Bench episode
- **WHEN** Nuveris Core validates the slice
- **THEN** stable entry identifiers and required provenance are checked
- **AND** relations, constraints, policies, runtime evaluations, and projection references resolve to entries in the slice
- **AND** missing, duplicate, or dangling references are returned as addressed validation findings

### Requirement: Operational State Transition Model
The system SHALL represent initial operational state, actor-specific observations, proposed and committed transitions, transition constraints, and acceptable or prohibited outcomes as serializable values.

#### Scenario: Validate an episode's resulting state
- **GIVEN** initial state, transition expectations, evidence of actions and committed transitions, and outcome expectations
- **WHEN** the episode is evaluated
- **THEN** the evaluator determines whether observed transitions were permitted
- **AND** it determines whether the resulting state is acceptable or prohibited
- **AND** missing state evidence, delayed effects, side effects, and unresolved outcomes can be reported without relying on a live clock
