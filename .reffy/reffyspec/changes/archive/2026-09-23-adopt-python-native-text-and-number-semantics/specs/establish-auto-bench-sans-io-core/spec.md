## MODIFIED Requirements

### Requirement: Agentic Trace Model

The system SHALL normalize validation evidence for submitted intent, LogicalAssembly selection and consultation, Lasm projections, actor observations, harness behavior, skill usage, MCP usage, policy checks, permissions, human confirmations, handoffs, proposed or committed state transitions, runtime Lasm evaluations, observed outcomes, evidence links, and failure attribution. The Python implementation SHALL preserve the existing event vocabulary, finding codes and paths, and evidence-reference behavior. It SHALL use Python semantics rather than JavaScript emulation for blank values, sequence ordering, and number spelling.

#### Scenario: Normalize evidence for evaluating a Lasm

- **GIVEN** evidence events from an Auto Bench episode
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

### Requirement: Migration Behavioral Parity

The migration SHALL record TypeScript source provenance and a language-independent corpus of inputs and reference outputs before retiring the existing implementation. The corpus SHALL cover every public behavioral function, existing behavioral tests, and migration-sensitive ordering, omission, scalar-type, invalid-input, and nested-evidence cases within the supported JSON domain. The recorded corpus SHALL remain unedited. Python results SHALL match the recorded reference after applying reviewed deviations; each deviation SHALL name its case, state its reason, and specify its change as patch operations, with no unexplained differences. Comparison SHALL preserve JSON scalar types and all ordered result content; it MAY ignore object-key order and equivalent JSON numeric spelling. Set-valued helper results SHALL use an explicit corpus encoding and compare membership without relaxing order checks for domain or result arrays.

#### Scenario: Verify the implementation against the recorded reference

- **GIVEN** a corpus produced by the recorded TypeScript source revision and any recorded working-tree patch
- **WHEN** the Python implementation evaluates the same inputs
- **THEN** outputs match the reference, with reviewed deviations applied, in event order and positions, finding order, codes, severity, paths, messages, attribution, IDs, evidence references, dimensions, and aggregate flags
- **AND** missing properties remain distinguishable from explicit nulls and booleans remain distinguishable from numbers
- **AND** expected outputs are not regenerated from Python to conceal mismatches

#### Scenario: A deliberate behavior change is recorded as a deviation

- **GIVEN** an intentional change makes a Python result differ from the recorded reference
- **WHEN** the change is implemented
- **THEN** a deviation entry records the case, the reason, and the patch against the recorded expected value
- **AND** entries for unknown cases, entries without a reason, and entries that change nothing fail the test suite
- **AND** any difference without such an entry fails the parity test
