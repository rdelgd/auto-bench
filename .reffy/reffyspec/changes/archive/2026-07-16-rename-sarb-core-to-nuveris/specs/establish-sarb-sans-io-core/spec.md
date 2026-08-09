## MODIFIED Requirements

### Requirement: TypeScript Sans I/O Core
The system SHALL provide a TypeScript core named **Nuveris Core**, with package identity `@nuveris/core`, whose domain modeling, validation, trace normalization, and evaluation behavior remain deterministic and independent of filesystem, network, process, database, clock, and live MCP access.

#### Scenario: Consume Nuveris Core from materialized inputs
- **GIVEN** a benchmark scenario, harness descriptors, codified skill descriptors, MCP surface descriptors, and trace events are already materialized as TypeScript values
- **WHEN** a consumer imports and invokes `@nuveris/core`
- **THEN** the core returns structured validation and evaluation results
- **AND** its package metadata and public documentation identify it as Nuveris Core rather than the SArB core
- **AND** it does not read files, call the network, access a database, inspect environment variables, or connect to a live MCP server

### Requirement: Scenario Model
The system SHALL model a Nuveris benchmark scenario as a serializable fixture containing business context, expected user intent, expected agentic control surfaces, and evaluation expectations, while allowing SArB to supply automotive benchmark scenarios using that model.

#### Scenario: Define an SArB automotive benchmark case with Nuveris
- **GIVEN** an SArB scenario for an automotive business workflow
- **WHEN** the scenario is represented with Nuveris Core
- **THEN** it includes a stable scenario id, human-readable title, business context, user intent, expected outcomes, and references to relevant harness, skill, and MCP fixtures
- **AND** it can be validated without requiring any external datastore or runtime integration
- **AND** SArB remains the benchmark identity rather than the core package identity

### Requirement: Harness Model
The system SHALL represent harnesses as first-class Nuveris fixtures describing the runtime or product surface that hosts, frames, or mediates the agent abstraction.

#### Scenario: Model a harness with Nuveris
- **GIVEN** a harness such as a coding harness, workflow harness, support harness, or future internal harness
- **WHEN** the harness is represented with Nuveris Core
- **THEN** the fixture captures a stable harness id, name, purpose, interaction mode, available context surfaces, tool or workspace affordances, permission model, approval flow, and handoff boundaries needed for evaluation
- **AND** evaluators can determine whether harness behavior helped or constrained the agent in a scenario-relevant way

### Requirement: Codified Skill Model
The system SHALL represent skills as first-class Nuveris fixtures describing the codified workflow surface available to an agent.

#### Scenario: Model a skill with Nuveris
- **GIVEN** a skill that has been codified for organizational use
- **WHEN** the skill is represented with Nuveris Core
- **THEN** the fixture captures a stable skill id, name, purpose, trigger or applicability metadata, declared capabilities, and optional references to supporting instructions or assets
- **AND** evaluators can determine whether the trace activated or relied on the skill in a scenario-relevant way

### Requirement: MCP Surface Model
The system SHALL represent MCP servers and primitives as first-class Nuveris fixtures describing the tools, resources, and prompts exposed to an agent.

#### Scenario: Model MCP primitives with Nuveris
- **GIVEN** an MCP server surface relevant to a benchmark scenario
- **WHEN** the surface is represented with Nuveris Core
- **THEN** the fixture captures the server identity and the exposed tool, resource, and prompt descriptors needed for evaluation
- **AND** the core can compare trace events against those descriptors without connecting to the live server
