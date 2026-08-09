## MODIFIED Requirements

### Requirement: TypeScript Sans I/O Core
The system SHALL provide a TypeScript core named **Nuveris Core**, with package identity `@nuveris/core`, whose domain modeling, validation, trace normalization, and evaluation behavior remain deterministic and independent of filesystem, network, process, database, clock, and live MCP access.

#### Scenario: Consume Nuveris Core from materialized inputs
- **GIVEN** a benchmark scenario, harness descriptors, codified skill descriptors, MCP surface descriptors, and trace events are already materialized as TypeScript values
- **WHEN** a consumer imports and invokes `@nuveris/core`
- **THEN** the core returns structured validation and evaluation results
- **AND** its package metadata and public documentation identify it as Nuveris Core rather than the Auto Bench core
- **AND** it does not read files, call the network, access a database, inspect environment variables, or connect to a live MCP server

### Requirement: Scenario Model
The system SHALL model a Nuveris benchmark scenario as a serializable fixture containing business context, expected user intent, expected agentic control surfaces, and evaluation expectations, while allowing Auto Bench to supply automotive benchmark scenarios using that model.

#### Scenario: Define an Auto Bench automotive benchmark case with Nuveris
- **GIVEN** an Auto Bench scenario for an automotive business workflow
- **WHEN** the scenario is represented with Nuveris Core
- **THEN** it includes a stable scenario id, human-readable title, business context, user intent, expected outcomes, and references to relevant harness, skill, and MCP fixtures
- **AND** it can be validated without requiring any external datastore or runtime integration
- **AND** Auto Bench remains the benchmark identity rather than the core package identity
