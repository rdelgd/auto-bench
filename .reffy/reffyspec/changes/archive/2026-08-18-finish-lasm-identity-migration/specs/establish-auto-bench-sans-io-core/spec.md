## MODIFIED Requirements

### Requirement: Harness Model
The system SHALL represent harnesses as first-class Lasm projection fixtures describing the runtime or product surface that hosts, frames, or mediates agent action against a LogicalAssembly.

#### Scenario: Model a harness as a Lasm projection
- **GIVEN** a coding, workflow, support, or internal harness relevant to an Auto Bench episode
- **WHEN** the harness is represented with `@lasm/core`
- **THEN** the fixture captures a stable id, name, purpose, interaction mode, context surfaces, affordances, permission model, approval flow, and handoff boundaries
- **AND** those surfaces MAY reference the assembly entries and operational-state fields they project or enforce
- **AND** Auto Bench can determine whether harness behavior preserved or distorted the relevant Lasm meaning and authority

### Requirement: Codified Skill Model
The system SHALL represent skills as first-class Lasm projection fixtures describing codified workflow surfaces available to an agent.

#### Scenario: Model a skill as a Lasm projection
- **GIVEN** a skill codified for organizational use
- **WHEN** the skill is represented with `@lasm/core`
- **THEN** the fixture captures a stable id, name, purpose, applicability, declared capabilities, and optional supporting references
- **AND** it MAY reference the assembly entries and operational-state fields projected by the workflow
- **AND** Auto Bench can determine whether the skill was activated and preserved the relevant Lasm meaning

### Requirement: MCP Surface Model
The system SHALL represent MCP servers and primitives as first-class Lasm projection fixtures describing tools, resources, and prompts exposed to an agent.

#### Scenario: Model MCP primitives as Lasm projections
- **GIVEN** an MCP surface relevant to an Auto Bench episode
- **WHEN** the surface is represented with `@lasm/core`
- **THEN** the fixture captures the server identity and exposed tool, resource, and prompt descriptors needed for evaluation
- **AND** each surface or primitive MAY reference the assembly entries and operational-state fields it exposes or changes
- **AND** Auto Bench can compare evidence against those descriptors without connecting to a live server
