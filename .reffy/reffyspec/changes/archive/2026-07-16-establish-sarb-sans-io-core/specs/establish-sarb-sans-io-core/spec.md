## ADDED Requirements
### Requirement: TypeScript Sans I/O Core
The system SHALL provide an initial TypeScript core for SArB whose domain modeling, validation, trace normalization, and evaluation behavior are deterministic and independent of filesystem, network, process, database, clock, and live MCP access.

#### Scenario: Evaluate from materialized inputs
- **GIVEN** a benchmark scenario, harness descriptors, codified skill descriptors, MCP surface descriptors, and trace events are already materialized as TypeScript values
- **WHEN** the core evaluates those values
- **THEN** it returns structured validation and evaluation results
- **AND** it does not read files, call the network, access a database, inspect environment variables, or connect to a live MCP server

### Requirement: Scenario Model
The system SHALL model a SArB scenario as a serializable benchmark fixture containing business context, expected user intent, expected agentic control surfaces, and evaluation expectations.

#### Scenario: Define an automotive benchmark case
- **GIVEN** a scenario for an automotive business workflow
- **WHEN** the scenario is represented in the core model
- **THEN** it includes a stable scenario id, human-readable title, business context, user intent, expected outcomes, and references to relevant harness, skill, and MCP fixtures
- **AND** it can be validated without requiring any external datastore or runtime integration

### Requirement: Harness Model
The system SHALL represent harnesses as first-class benchmark fixtures describing the runtime or product surface that hosts, frames, or mediates the agent abstraction.

#### Scenario: Model a harness mediating an agent
- **GIVEN** a harness such as a coding harness, workflow harness, support harness, or future internal harness
- **WHEN** the harness is represented in SArB
- **THEN** the fixture captures a stable harness id, name, purpose, interaction mode, available context surfaces, tool or workspace affordances, permission model, approval flow, and handoff boundaries needed for evaluation
- **AND** evaluators can determine whether harness behavior helped or constrained the agent in a scenario-relevant way

### Requirement: Codified Skill Model
The system SHALL represent skills as first-class benchmark fixtures describing the codified workflow surface available to an agent.

#### Scenario: Model a skill available to an agent
- **GIVEN** a skill that has been codified for organizational use
- **WHEN** the skill is represented in SArB
- **THEN** the fixture captures a stable skill id, name, purpose, trigger or applicability metadata, declared capabilities, and optional references to supporting instructions or assets
- **AND** evaluators can determine whether the trace activated or relied on the skill in a scenario-relevant way

### Requirement: MCP Surface Model
The system SHALL represent MCP servers and primitives as first-class benchmark fixtures describing the tools, resources, and prompts exposed to an agent.

#### Scenario: Model MCP primitives exposed during a scenario
- **GIVEN** an MCP server surface relevant to a benchmark scenario
- **WHEN** the surface is represented in SArB
- **THEN** the fixture captures the server identity and the exposed tool, resource, and prompt descriptors needed for evaluation
- **AND** the core can compare trace events against those descriptors without connecting to the live server

### Requirement: Agentic Trace Model
The system SHALL normalize agentic trace events for intent, harness behavior, skill usage, MCP usage, policy checks, human confirmations, handoffs, and task outcomes.

#### Scenario: Normalize harness, skill, and MCP trace events
- **GIVEN** a trace containing events for submitted intent, harness selection, harness context loading, harness permission decisions, skill activation, MCP primitive listing, tool calls, resource reads, policy checks, human confirmation, and task completion
- **WHEN** the trace is processed by the core
- **THEN** the core returns a normalized event sequence with stable event types, timestamps or sequence positions, actor identifiers, subject identifiers, and evidence payloads
- **AND** malformed or unknown events are reported as validation findings rather than causing hidden side effects

### Requirement: Structured Evaluation Results
The system SHALL evaluate a scenario trace against the modeled harnesses, skills, and MCP surfaces using structured dimensions for intent fidelity, control surface quality, business realism, observability, and governance.

#### Scenario: Evaluate an agentic benchmark run
- **GIVEN** a valid scenario, relevant harness fixtures, relevant skill fixtures, relevant MCP fixtures, and a normalized trace
- **WHEN** the evaluator runs
- **THEN** it returns per-dimension results with status, findings, and evidence references
- **AND** it distinguishes user intent, agent inference, harness behavior, available control primitives, selected control primitives, policy constraints, and final business outcome where the trace provides enough evidence

### Requirement: Data Handling Deferral
The system SHALL keep persistence, ingestion, transport, UI, organization-wide analytics collection, and live agent execution outside the initial core boundary.

#### Scenario: Add a future adapter
- **GIVEN** a future adapter that loads scenarios from files, databases, APIs, event streams, or MCP servers
- **WHEN** the adapter invokes the core
- **THEN** it passes materialized domain values into the core
- **AND** the core returns materialized validation and evaluation values without taking ownership of storage, transport, ingestion, or runtime orchestration
