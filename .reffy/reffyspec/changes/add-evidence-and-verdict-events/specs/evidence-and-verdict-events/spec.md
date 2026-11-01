## ADDED Requirements

### Requirement: Evidence and Verdict Event Types

The system SHALL define version 1 ledger data schemas for four event types:

- `evidence.recorded`: a measurement, carrying its cell id, attempt, optional shard index and count, target, vindex pin, patch digest, patchrig commit, larql version, manipulation check, tier, scope, controls state, free-form measurements, records digest, environment, and optional ledger position.
- `verdict.recorded`: a judgement, carrying its cell id, attempt, a citation of one measurement event, pre-registration, scorer version, an optional superseded verdict stream, a verdict, an optional cannot-tell reason, optional detail, and an optional policy event citation.
- `verdict.invalidated`: an instrument, a scope of patchrig commits, vindex pins, and larql versions, a citation of one affected verdict event, and a reason.
- `invalidation.retracted`: a citation of one invalidation stream, as a stream id, and a reason.

Keys SHALL be camelCase, enum values kebab-case, and absent optional fields omitted rather than null. The verdict SHALL be one of `holds`, `inconclusive`, `fails`, or `cannot-tell`. A `cannot-tell` verdict SHALL carry a `cannotTellReason` from the closed set `no-probes`, `too-few-values`, `degenerate-stratum`, `instrument-gate-failed`, and `no-eligible-chains`, and no other verdict SHALL carry one. The checked-in schemas, the pure validator, and `jsonschema` SHALL agree on every accept or reject decision.

#### Scenario: Validate a cannot-tell verdict

- **GIVEN** `verdict.recorded` data with verdict `cannot-tell`
- **WHEN** `validate_ledger_event_data` runs
- **THEN** data with `cannotTellReason` `degenerate-stratum` and an optional `detail` is valid
- **AND** data without a reason is rejected with `verdict.reason_required`
- **AND** data with a reason outside the five codes is rejected
- **AND** `jsonschema` with the checked-in schema reaches the same verdicts

#### Scenario: Reject a reason on any other verdict

- **GIVEN** `verdict.recorded` data with verdict `holds`, `inconclusive`, or `fails`
- **WHEN** it carries a `cannotTellReason`
- **THEN** it is rejected with `verdict.reason_not_allowed` at `data.cannotTellReason`

#### Scenario: Reject superseded vocabulary and nulls

- **GIVEN** `verdict.recorded` data with verdict `holds-weakly` or `holds_weakly`, or with `supersedes` set to null
- **WHEN** `validate_ledger_event_data` runs
- **THEN** the data is rejected with a structured format finding

### Requirement: Verdict Projection

The system SHALL provide `project_verdicts(events)`, a pure projection over events in global-log order. It SHALL read only event types and data, never parse stream ids, and ignore event types it does not own. It SHALL fold verdicts per (cell id, pre-registration) and never across pre-registrations. Within one group, a verdict whose `supersedes` names another verdict stream in the same group SHALL remove it. An invalidation SHALL remove every verdict it cites and every verdict whose cited measurement matches its scope, where every present, non-empty scope list must contain the measurement's corresponding value. An invalidation SHALL apply only while no retraction cites its stream. Each group SHALL be reported as `current` with exactly one verdict, `invalidated` when invalidations removed all remaining verdicts, or `conflicting` with its candidates and a finding. The projection SHALL NOT break ties, interpret detail, measurements, or the manipulation check, order dates, or consult a clock.

#### Scenario: A re-score supersedes the original

- **GIVEN** a measurement, a verdict on it, and a second verdict for the same cell and pre-registration whose `supersedes` names the first verdict's stream
- **WHEN** the events are projected
- **THEN** the group is `current` with the second verdict, citing its source event and the measurement

#### Scenario: Pre-registrations never fold together

- **GIVEN** two unsuperseded verdicts for one cell under two different pre-registrations
- **WHEN** the events are projected
- **THEN** each pre-registration has its own `current` group
- **AND** no conflict is reported

#### Scenario: Report a conflict instead of breaking a tie

- **GIVEN** two verdicts for one cell and pre-registration, neither superseding the other
- **WHEN** the events are projected
- **THEN** the group is `conflicting`, lists both verdict events as candidates, and has no current verdict
- **AND** a `verdict.conflict` finding is reported

#### Scenario: An invalidation's condition reaches later verdicts

- **GIVEN** an invalidation whose scope names larql version `0.2.0`
- **AND** a verdict written after it, citing a measurement taken with larql `0.2.0`, which the invalidation does not cite
- **WHEN** the events are projected
- **THEN** that verdict is removed, and its group lists the invalidation stream in `invalidatedBy`
- **AND** a verdict whose measurement used another larql version is unaffected

#### Scenario: A retraction restores what an invalidation removed

- **GIVEN** an invalidation that removed a group's only verdict, and an `invalidation.retracted` citing that invalidation's stream
- **WHEN** the events are projected
- **THEN** the group is `current` with that verdict again

#### Scenario: Report events the projection cannot trust

- **GIVEN** a verdict citing a measurement absent from the log, a `supersedes` naming an unknown stream or another group's verdict, an invalidation with an empty scope or with inconsistent conditions across its events, a retraction of an unknown stream, or an event with an unsupported version or invalid data
- **WHEN** the events are projected
- **THEN** each produces its addressed finding
- **AND** a verdict with an unknown measurement is not a candidate
- **AND** an empty scope matches by citation only, never every verdict

#### Scenario: Project without I/O, deterministically

- **GIVEN** the same events, including foreign event types
- **WHEN** they are projected repeatedly, with file, environment, network, process, and clock access unavailable
- **THEN** each result serializes identically, groups are sorted by cell id and pre-registration, and the input events are unchanged
