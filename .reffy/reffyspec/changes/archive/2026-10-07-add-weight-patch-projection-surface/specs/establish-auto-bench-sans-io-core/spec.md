## ADDED Requirements

### Requirement: Weight Patch Projection Model

The system SHALL represent compiled knowledge patches applied to a model's weights as first-class Lasm projection fixtures. A weight patch descriptor SHALL carry a stable id, name, purpose, the identity of the base model it patches, a content digest, and a required projection reference naming the assembly entries and operational-state fields the patch claims to carry. The core SHALL NOT compute digests, compile, serve, or probe patches, or represent patch methods or rig configuration.

#### Scenario: Model a weight patch as a Lasm projection

- **GIVEN** a compiled knowledge patch that a fleet's model carries for an Auto Bench episode
- **WHEN** the patch is represented with `lasm_core`
- **THEN** the fixture captures its id, name, purpose, base model identity, digest, and projection references
- **AND** validation reports a missing required field, an empty projection, or a projection reference that does not resolve to the supplied assembly or state
- **AND** no filesystem, network, model, or rig access is required to validate it

#### Scenario: Treat the digest as the identity of the deployed surface

- **GIVEN** a conformance case with a modeled weight patch and a trace containing a `patch.applied` event for that patch
- **WHEN** Auto Bench evaluates the case
- **THEN** an applied digest equal to the descriptor's digest produces no finding
- **AND** an applied digest different from the descriptor's digest produces a control-surface-quality error attributed to the control surface
- **AND** the assembly and the reality-model-validity dimension are not blamed for the mismatch

#### Scenario: Treat a failed probe as projection loss

- **GIVEN** a modeled weight patch claiming an assembly entry and a `patch.probed` event for that patch whose evidence does not record `passed` as `true`
- **WHEN** Auto Bench evaluates the case
- **THEN** a control-surface-quality error attributed to the projection addresses the patch's projected entry ids
- **AND** a probe recorded as passed produces no finding

#### Scenario: Name the patch when a projected entry diverges

- **GIVEN** a `lasm.divergence_detected` event whose subject is an assembly entry projected by one or more modeled weight patches
- **WHEN** Auto Bench evaluates the case
- **THEN** in addition to the existing divergence finding, a semantic-fidelity error attributed to the projection names each such patch id
- **AND** a divergence on an entry projected only by harness, skill, or MCP surfaces produces no such finding

#### Scenario: Leave existing cases unchanged

- **GIVEN** a conformance case with no weight patches and no `patch.*` events, including every recorded corpus case and the service-scheduling fixture
- **WHEN** Auto Bench evaluates the case
- **THEN** every validation finding and dimension result is identical to the result before this capability existed

## MODIFIED Requirements

### Requirement: Scenario Model

The system SHALL model an Auto Bench episode as a serializable fixture containing business context, expected user intent, an episode-scoped LogicalAssembly reference set, expected Lasm projections and control surfaces including harnesses, skills, MCP servers, MCP primitives, and weight patches, initial operational state, actor-relevant observations, permitted or prohibited transitions, acceptable or prohibited outcomes, and evaluation expectations. Expected weight patch ids MAY be omitted, and omission SHALL mean none are expected.

#### Scenario: Define an automotive Lasm evaluation episode

- **GIVEN** an Auto Bench episode for an automotive business workflow
- **WHEN** the episode is represented with `lasm_core`
- **THEN** it identifies the assembly version and entries governing the episode
- **AND** it defines the initial state and the state transitions and outcomes needed to judge success or failure
- **AND** it references the harness, skill, MCP, weight patch, and authority projections through which the agent encounters or changes that reality
- **AND** it can be validated without an external datastore or runtime integration

#### Scenario: Expect a weight patch

- **GIVEN** a scenario whose expected control surfaces name a weight patch id
- **WHEN** the conformance case is validated
- **THEN** an expected id with no matching weight patch fixture is reported as a scenario reference finding
- **AND** duplicate ids across harnesses, skills, MCP servers, MCP primitives, and weight patches are reported once each

### Requirement: Lasm Projection Model

The system SHALL represent agent-facing harness, skill, MCP, weight patch, prompt, permission, approval, and handoff surfaces as projections or controls that MAY reference the LogicalAssembly entries and operational-state contracts they expose or enforce. A weight patch SHALL reference at least one entry or state field.

#### Scenario: Attribute a lossy agent-facing projection

- **GIVEN** an agent-facing surface references the assembly meaning it projects or enforces
- **WHEN** Auto Bench evidence shows that the surface omitted, distorted, or contradicted that meaning
- **THEN** the evaluator can attribute the divergence to the projection or control surface
- **AND** no separately named middle-layer model is required to connect the surface to the LogicalAssembly

#### Scenario: Count a weight patch toward reality coverage

- **GIVEN** a relevant assembly entry is projected only by a modeled weight patch
- **WHEN** Auto Bench evaluates reality coverage
- **THEN** the entry is treated as projected
- **AND** removing the patch from the case makes the entry absent from agent-facing projections

### Requirement: Agentic Trace Model

The system SHALL normalize validation evidence for submitted intent, LogicalAssembly selection and consultation, Lasm projections, actor observations, harness behavior, skill usage, MCP usage, weight patch application and probing, policy checks, permissions, human confirmations, handoffs, proposed or committed state transitions, runtime Lasm evaluations, observed outcomes, evidence links, and failure attribution. The event vocabulary SHALL include `patch.applied` and `patch.probed`, whose subject is the weight patch id. The Python implementation SHALL preserve the existing finding codes and paths and evidence-reference behavior, and SHALL use Python semantics rather than JavaScript emulation for blank values, sequence ordering, and number spelling. The addition of event types SHALL be recorded as a reviewed parity deviation for the event-type constant.

#### Scenario: Normalize evidence for evaluating a Lasm

- **GIVEN** evidence events from an Auto Bench episode, including `patch.applied` and `patch.probed`
- **WHEN** the evidence is normalized
- **THEN** each accepted event has a stable type, position, actor, optional subject, and evidence payload
- **AND** the normalized sequence can distinguish represented reality, projected meaning, observed state, agent inference, proposed action, committed transition, runtime Lasm evaluation, Auto Bench evaluation evidence, and validated outcome
- **AND** malformed or unknown evidence is reported as validation findings rather than causing hidden side effects

#### Scenario: Order and address sequenced and unsequenced evidence

- **GIVEN** raw events with numeric or omitted sequences, equal-sequence ties, unknown types, and missing actors
- **WHEN** the Python normalizer processes the materialized trace
- **THEN** numbered events are ordered by sequence, followed by every unsequenced event, with ties kept in original input order
- **AND** accepted events receive consecutive one-based positions and `trace:<position>` references
- **AND** normalization findings refer to the original input indices
- **AND** trace validation retains its distinct reporting of invalid or duplicate sequences

#### Scenario: Apply Python value semantics

- **GIVEN** required strings or trace actors containing only characters that Python's `str.strip()` removes, or trace sequences `1` and `1.0`
- **WHEN** validation or normalization runs
- **THEN** those strings are treated as blank and reported as missing
- **AND** `1` and `1.0` are the same valid integer sequence and are reported as a duplicate
- **AND** duplicate-sequence messages spell the value with Python's `str()`

#### Scenario: Record the event vocabulary change as a deviation

- **GIVEN** the recorded corpus case for the event-type constant
- **WHEN** the parity suite runs after the two patch events are added
- **THEN** a deviation entry under this change id explains the difference and changes the recorded expectation
- **AND** every other recorded case matches without a new deviation

### Requirement: Structured Evaluation Results

The system SHALL enable Auto Bench to evaluate a Lasm using structured dimensions for intent fidelity, semantic fidelity, reality-model validity, state and outcome validity, control-surface quality, reality coverage, evidence and attribution, and governance. Control-surface quality SHALL check expected, unmodeled, and unused weight patches alongside harnesses, skills, and MCP surfaces, and SHALL report digest mismatches and failed probes. Semantic fidelity SHALL name the weight patches projecting a diverged entry. The result vocabulary, dimension ordering, finding record shape, attribution values, and aggregation of validity and conformance SHALL otherwise be preserved.

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

#### Scenario: Evaluate the new-vehicle-units reference episode

- **GIVEN** the sales-domain reference fixture in which a weight patch claims the net new-vehicle units and stock type concepts, is applied with its recorded digest, passes a canonical probe, fails a paraphrase probe, and the agent reports a retail-only count
- **WHEN** Auto Bench evaluates the fixture
- **THEN** control-surface quality fails with a probe-failure finding attributed to the projection and addressing the units concept
- **AND** semantic fidelity fails with a finding that names the patch id
- **AND** state and outcome validity fails with the prohibited outcome
- **AND** the evaluation is repeatable and leaves the fixture unchanged

### Requirement: Versioned JSON Interchange

The system SHALL define versioned JSON Schemas for logical assemblies, conformance cases, raw traces, trace-normalization results, validation results, and conformance evaluations, including their constituent public domain records. Version 1 documents SHALL use `schemaVersion`, `kind`, and `value` fields. The format version SHALL be independent of the package version and assembly version. Additive optional properties and additive enum values MAY be introduced within version 1 when omitted fields keep their prior meaning; the weight patch descriptor, the optional `weightPatches` and `weightPatchIds` properties, and the `patch.*` event types are such additions. Pure interchange helpers SHALL preserve current payload vocabulary and return structured format findings for unsupported versions, kinds, invalid JSON, or incompatible shapes without performing external I/O.

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

#### Scenario: Accept and reject weight patch content within version 1

- **GIVEN** a version 1 conformance-case document
- **WHEN** it includes a `weightPatches` array of well-formed descriptors and an `expectedControlSurfaces.weightPatchIds` list
- **THEN** it is accepted with `schemaVersion` 1 and decodes to a payload that `evaluate_conformance` accepts
- **AND** a document that omits both properties decodes to the same payload it did before this change
- **AND** a descriptor missing `projection`, `digest`, or `baseModelId`, or carrying an unknown property, is rejected with a structured format finding
- **AND** a descriptor whose `projection` lists no entries and no state fields is admitted by the schema and reported by `validate_weight_patch`
