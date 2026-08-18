## MODIFIED Requirements

### Requirement: TypeScript Sans I/O Core
The system SHALL provide a TypeScript core named **Nuveris Core**, with package identity `@nuveris/core`, whose conformance-case modeling, validation, trace normalization, and evaluation behavior remain deterministic and independent of filesystem, network, process, database, clock, and live MCP access.

#### Scenario: Consume Nuveris Core from materialized conformance inputs
- **GIVEN** a conformance scenario, harness descriptors, codified skill descriptors, MCP surface descriptors, and trace events are already materialized as TypeScript values
- **WHEN** a consumer invokes `evaluateConformance` with a `ConformanceCase`
- **THEN** the core returns a structured `ConformanceEvaluation`
- **AND** its package metadata and public documentation identify conformance rather than competitive benchmarking as the core responsibility
- **AND** it does not read files, call the network, access a database, inspect environment variables, or connect to a live MCP server

### Requirement: Scenario Model
The system SHALL model a Nuveris conformance scenario as a serializable fixture containing business context, expected user intent, expected agentic control surfaces, and evaluation expectations, while allowing Auto Bench to supply automotive conformance cases using that model.

#### Scenario: Define an Auto Bench automotive conformance case with Nuveris
- **GIVEN** an Auto Bench conformance case for an automotive business workflow
- **WHEN** its scenario is represented with Nuveris Core
- **THEN** it includes a stable scenario id, human-readable title, business context, user intent, expected outcomes, and references to relevant harness, skill, and MCP fixtures
- **AND** it can be validated without requiring any external datastore or runtime integration
- **AND** Auto Bench remains the automotive workbench identity rather than the core package identity

### Requirement: Structured Evaluation Results
The system SHALL evaluate a conformance case against the modeled scenario, harnesses, skills, MCP surfaces, and agentic trace using structured dimensions for intent fidelity, control-surface quality, operational grounding, observability, and governance.

#### Scenario: Evaluate an agentic conformance case
- **GIVEN** a valid `ConformanceCase` containing a scenario, relevant harness fixtures, relevant skill fixtures, relevant MCP fixtures, and a trace
- **WHEN** `evaluateConformance` runs
- **THEN** it returns a `ConformanceEvaluation` with per-dimension results, status, findings, and evidence references
- **AND** the operational-grounding dimension determines whether required operational facts are evidenced
- **AND** it distinguishes user intent, agent inference, harness behavior, available control primitives, selected control primitives, policy constraints, and final business outcome where the trace provides enough evidence
- **AND** no benchmark-oriented aliases are required for the private pre-release package
