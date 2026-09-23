## RENAMED Requirements

- FROM: `### Requirement: TypeScript Sans I/O Core`
- TO: `### Requirement: Python Sans I/O Core`

## MODIFIED Requirements

### Requirement: Python Sans I/O Core

The system SHALL provide a reusable Python library named **Lasm**, with distribution name `lasm-core` and import namespace `lasm_core`, whose LogicalAssembly modeling, agent-facing projection modeling, reality-validation domain modeling, evidence normalization, validation, and deterministic evaluation mechanics remain independent of filesystem, network, process, database, clock, live agent, and live MCP access. Its domain functions SHALL consume and return materialized values without mutating caller inputs. Active package metadata, documentation, specifications, workspace identifiers, and examples SHALL identify the library as Lasm; archived planning records MAY retain historical identities.

#### Scenario: Consume Lasm from materialized reality-validation inputs

- **GIVEN** an episode-scoped LogicalAssembly slice, Auto Bench episode, operational state contract, agent-facing projections, and evidence events are materialized as typed Python values
- **WHEN** a consumer imports `lasm_core` and invokes its domain functions
- **THEN** the library returns structured validation and evaluation values that Auto Bench can use to evaluate the Lasm
- **AND** it does not resolve remote assembly entries, read application data files, call the network, access a database, inspect environment variables, start a process, execute an agent, or connect to a live MCP server
- **AND** it does not require Node.js or a platform SDK
- **AND** its active public identity does not introduce a separately named semantic-control middle layer

#### Scenario: Repeat an evaluation without changing inputs

- **GIVEN** a materialized conformance case, including nested evidence and assembly records
- **WHEN** `evaluate_conformance` is invoked repeatedly with that case
- **THEN** the serialized results are equivalent on every invocation
- **AND** the input case and its nested values are unchanged
- **AND** no live clock or global mutable state affects the result

### Requirement: Scenario Model

The system SHALL model an Auto Bench episode as a serializable fixture containing business context, expected user intent, an episode-scoped LogicalAssembly reference set, expected Lasm projections and control surfaces, initial operational state, actor-relevant observations, permitted or prohibited transitions, acceptable or prohibited outcomes, and evaluation expectations.

#### Scenario: Define an automotive Lasm evaluation episode

- **GIVEN** an Auto Bench episode for an automotive business workflow
- **WHEN** the episode is represented with `lasm_core`
- **THEN** it identifies the assembly version and entries governing the episode
- **AND** it defines the initial state and the state transitions and outcomes needed to judge success or failure
- **AND** it references the harness, skill, MCP, and authority projections through which the agent encounters or changes that reality
- **AND** it can be validated without an external datastore or runtime integration

### Requirement: Harness Model

The system SHALL represent harnesses as first-class Lasm projection fixtures describing the runtime or product surface that hosts, frames, or mediates agent action against a LogicalAssembly.

#### Scenario: Model a harness as a Lasm projection

- **GIVEN** a coding, workflow, support, or internal harness relevant to an Auto Bench episode
- **WHEN** the harness is represented with `lasm_core`
- **THEN** the fixture captures a stable id, name, purpose, interaction mode, context surfaces, affordances, permission model, approval flow, and handoff boundaries
- **AND** those surfaces MAY reference the assembly entries and operational-state fields they project or enforce
- **AND** Auto Bench can determine whether harness behavior preserved or distorted the relevant Lasm meaning and authority

### Requirement: Codified Skill Model

The system SHALL represent skills as first-class Lasm projection fixtures describing codified workflow surfaces available to an agent.

#### Scenario: Model a skill as a Lasm projection

- **GIVEN** a skill codified for organizational use
- **WHEN** the skill is represented with `lasm_core`
- **THEN** the fixture captures a stable id, name, purpose, applicability, declared capabilities, and optional supporting references
- **AND** it MAY reference the assembly entries and operational-state fields projected by the workflow
- **AND** Auto Bench can determine whether the skill was activated and preserved the relevant Lasm meaning

### Requirement: MCP Surface Model

The system SHALL represent MCP servers and primitives as first-class Lasm projection fixtures describing tools, resources, and prompts exposed to an agent.

#### Scenario: Model MCP primitives as Lasm projections

- **GIVEN** an MCP surface relevant to an Auto Bench episode
- **WHEN** the surface is represented with `lasm_core`
- **THEN** the fixture captures the server identity and exposed tool, resource, and prompt descriptors needed for evaluation
- **AND** each surface or primitive MAY reference the assembly entries and operational-state fields it exposes or changes
- **AND** Auto Bench can compare evidence against those descriptors without connecting to a live server

### Requirement: Agentic Trace Model

The system SHALL normalize validation evidence for submitted intent, LogicalAssembly selection and consultation, Lasm projections, actor observations, harness behavior, skill usage, MCP usage, policy checks, permissions, human confirmations, handoffs, proposed or committed state transitions, runtime Lasm evaluations, observed outcomes, evidence links, and failure attribution. The Python implementation SHALL preserve the existing event vocabulary, normalization ordering, event admission, finding paths, and evidence-reference behavior.

#### Scenario: Normalize evidence for evaluating a Lasm

- **GIVEN** evidence events from an Auto Bench episode
- **WHEN** the evidence is normalized
- **THEN** each accepted event has a stable type, position, actor, optional subject, and evidence payload
- **AND** the normalized sequence can distinguish represented reality, projected meaning, observed state, agent inference, proposed action, committed transition, runtime Lasm evaluation, Auto Bench evaluation evidence, and validated outcome
- **AND** malformed or unknown evidence is reported as validation findings rather than causing hidden side effects

#### Scenario: Preserve sequence and evidence addressing during the port

- **GIVEN** raw events with numeric or omitted sequences, equal-sequence ties, unknown types, and missing actors
- **WHEN** the Python normalizer processes the materialized trace
- **THEN** ordering and event admission match the recorded TypeScript reference, including its omitted-sequence sentinel and original-input-order tie breaking
- **AND** accepted events receive consecutive one-based positions and `trace:<position>` references
- **AND** normalization findings refer to the original input indices
- **AND** trace validation retains its distinct reporting of invalid or duplicate sequences

### Requirement: Structured Evaluation Results

The system SHALL enable Auto Bench to evaluate a Lasm using structured dimensions for intent fidelity, semantic fidelity, reality-model validity, state and outcome validity, control-surface quality, reality coverage, evidence and attribution, and governance. The Python implementation SHALL preserve the existing result vocabulary, dimension ordering, finding order and contents, attribution, evidence references, and aggregation of validity and conformance.

#### Scenario: Auto Bench evaluates the Lasm

- **GIVEN** a valid assembly slice, Auto Bench episode, initial state, Lasm projections, and normalized evidence
- **WHEN** the Auto Bench evaluator runs
- **THEN** it returns per-dimension status, findings, and evidence references
- **AND** it can attribute divergence to the reality model, a projection, a control surface, agent conduct, an external system, or insufficient evaluation evidence
- **AND** it treats Lasm runtime evaluation results as evidence rather than equating their passage with conformance of the Lasm as a whole
- **AND** it establishes outcomes from state and evidence rather than an agent's task-completion claim alone

#### Scenario: Preserve a nonconformant evaluation

- **GIVEN** a reference case with late confirmation, prohibited transitions or outcomes, stale provenance, or missing attribution
- **WHEN** the Python evaluator processes the same payload as the TypeScript reference
- **THEN** all validation findings and dimension results match the recorded reference, including messages and addressed IDs
- **AND** `valid` and `conformant` use the same warning and failure rules
- **AND** validation and normalization findings retain the existing deduplication behavior

### Requirement: Data Handling Deferral

The system SHALL keep source extraction and reconciliation, persistence, ingestion, transport, UI, generic agent analytics, dashboards, organization-wide telemetry collection, live agent execution, and live integrations outside the `lasm_core` boundary. Python platform, model, and agent integrations SHALL remain adapter concerns rather than prerequisites for core execution.

#### Scenario: Integrate external sources and telemetry through adapters

- **GIVEN** an adapter that compiles assembly entries, loads episode state, runs an agent, or imports telemetry from external systems
- **WHEN** the adapter invokes `lasm_core`
- **THEN** it passes materialized domain values and evidence into the library
- **AND** the library returns materialized validation and evaluation values without taking ownership of sources, storage, transport, collection, orchestration, or analytics presentation
- **AND** the same core call works without the adapter's SDKs, credentials, or live services

### Requirement: LogicalAssembly Slice Model

The system SHALL represent an immutable, serializable, episode-scoped LogicalAssembly slice with stable assembly identity, version, provenance, concepts, relations, constraints, events, policies, and runtime evaluation descriptors. Core operations SHALL treat supplied assembly records as immutable snapshots without changing their contents.

#### Scenario: Validate a materialized assembly slice

- **GIVEN** a materialized assembly slice for an Auto Bench episode
- **WHEN** `lasm_core` validates the slice
- **THEN** stable entry identifiers and required provenance are checked
- **AND** relations, constraints, policies, runtime evaluations, and projection references resolve to entries in the slice
- **AND** missing, duplicate, or dangling references are returned as addressed validation findings
- **AND** the supplied assembly is unchanged

## ADDED Requirements

### Requirement: Versioned JSON Interchange

The system SHALL define versioned JSON Schemas for logical assemblies, conformance cases, raw traces, trace-normalization results, validation results, and conformance evaluations, including their constituent public domain records. Version 1 documents SHALL use `schemaVersion`, `kind`, and `value` fields. The format version SHALL be independent of the package version and assembly version. Pure interchange helpers SHALL preserve current payload vocabulary and return structured format findings for unsupported versions, kinds, invalid JSON, or incompatible shapes without performing external I/O.

#### Scenario: Round-trip a materialized case and evaluation

- **GIVEN** a version 1 case document and its evaluation document conforming to the checked-in schemas
- **WHEN** their supplied JSON is decoded and encoded by the Python interchange helpers
- **THEN** payload names, IDs, scalar types, array ordering, findings, and evidence references are preserved
- **AND** omitted optional fields remain omitted while explicit nulls in JSON-valued fields remain null
- **AND** object-key ordering and textual whitespace MAY differ
- **AND** the decoded case payload can be passed directly to `evaluate_conformance`

#### Scenario: Reject an incompatible document before evaluation

- **GIVEN** supplied JSON with an unsupported version or kind, incompatible field types, unknown structural properties, non-finite numbers, or integer-valued numbers outside the safe range of -9007199254740991 through 9007199254740991
- **WHEN** an interchange helper validates the document
- **THEN** it reports structured format findings and supplies no accepted payload for evaluation
- **AND** it does not coerce booleans or strings to numbers, fill omitted fields, or guess a document version
- **AND** arbitrary JSON-compatible keys remain permitted inside declared evidence/value maps

#### Scenario: Preserve domain findings for semantically invalid payloads

- **GIVEN** a structurally valid document whose payload has empty required strings or arrays, dangling references, unknown raw event types, absent raw actors, or negative, fractional, or duplicate numeric sequences
- **WHEN** the document is decoded and the relevant domain validator is invoked
- **THEN** decoding preserves those values for semantic validation
- **AND** domain validation returns the existing addressed findings for the invalid values
- **AND** the wire layer does not substitute constructor exceptions or new business rules

### Requirement: Python API and Package Completeness

The system SHALL supply a typed Python equivalent for every current public domain type, constant, helper, validator, normalizer, evaluator, and reference-fixture export, documented in a migration inventory. The `lasm-core` wheel and source distributions SHALL support Python 3.11 and later declared supported versions, include typing metadata and versioned schema artifacts, and expose core and automotive fixtures separately as `lasm_core` and `lasm_core.fixtures`.

#### Scenario: Install and use the complete package outside the repository

- **GIVEN** a clean supported Python environment without Node.js or platform SDKs
- **WHEN** a consumer installs a locally built wheel or source distribution
- **THEN** the public core API and reference fixtures can be imported outside the source checkout
- **AND** the reference case can be validated and evaluated without external services or application data-file reads
- **AND** declared type information and schema artifacts are included in the installed distribution
- **AND** importing the core root does not initialize the reference fixture or run its evaluation

### Requirement: Migration Behavioral Parity

The migration SHALL record TypeScript source provenance and a language-independent corpus of inputs and reference outputs before retiring the existing implementation. The corpus SHALL cover every public behavioral function, existing behavioral tests, and migration-sensitive ordering, omission, scalar-type, invalid-input, and nested-evidence cases within the supported JSON domain. Python results SHALL match the reference with no unexplained differences. Comparison SHALL preserve JSON scalar types and all ordered result content; it MAY ignore object-key order and equivalent JSON numeric spelling. Set-valued helper results SHALL use an explicit corpus encoding and compare membership without relaxing order checks for domain or result arrays.

#### Scenario: Verify the port against the recorded reference

- **GIVEN** a corpus produced by the recorded TypeScript source revision and any recorded working-tree patch
- **WHEN** the Python implementation evaluates the same inputs
- **THEN** outputs match in event order and positions, finding order, codes, severity, paths, messages, attribution, IDs, evidence references, dimensions, and aggregate flags
- **AND** missing properties remain distinguishable from explicit nulls and booleans remain distinguishable from numbers
- **AND** expected outputs are not regenerated from Python to conceal mismatches

#### Scenario: A mismatch prevents retirement

- **GIVEN** a Python result differs from the reference for a supported input
- **WHEN** migration readiness is assessed
- **THEN** TypeScript retirement remains incomplete until the mismatch is explained and resolved
- **AND** unrelated changes to evaluation semantics are tracked separately from the language port

### Requirement: Single Canonical Core After Migration

After behavioral parity and Python package verification pass, the system SHALL make Python the sole maintained core implementation and retire the TypeScript core, npm package surface, and Node-based core development workflow. It SHALL retain the shared regression corpus, reference provenance, and migration documentation. Archived planning records SHALL remain unchanged. This migration SHALL NOT introduce an npm compatibility wrapper or a second maintained evaluator.

#### Scenario: Complete the implementation cutover

- **GIVEN** all parity and package checks pass and known consumer migrations have been accounted for
- **WHEN** the migration is completed
- **THEN** normal core builds, tests, fixture use, and evaluations require Python tooling and do not require Node.js
- **AND** active documentation and project conventions describe the Python package and its breaking import change
- **AND** regression coverage remains runnable against the recorded JSON corpus after TypeScript source removal
- **AND** TypeScript consumers can use the documented interchange contract through adapters without a promised in-process JavaScript evaluator
- **AND** the existing capability remains `establish-auto-bench-sans-io-core` with its purpose updated to describe Python at archival
