# evidence-and-verdict-events Specification

## Purpose
Define the meaning of version 1 evidence and verdict events in `lasm_core.verdict`: measurements, verdicts, invalidations, and retractions for weight-rig cells, and the `project_verdicts` projection of each (cell, attempt, pre-registration) group's current verdict, reported rather than guessed where it can't be resolved.

## Requirements

### Requirement: Evidence and Verdict Event Types

The system SHALL define version 1 ledger data schemas for four event types:

- `evidence.recorded`: a measurement, carrying its cell id (without the attempt), attempt, optional shard index and count, target, vindex pin, patch digest, patchrig commit, larql version, larql binary digest, manipulation check, tier, claim scope, controls state, free-form measurements, records digest, environment, and optional ledger position.
- `verdict.recorded`: a judgement, carrying its cell id, attempt, a citation of one measurement event, pre-registration, scorer version, an optional superseded verdict stream, a verdict, an optional cannot-tell reason, optional detail, and an optional policy event citation.
- `verdict.invalidated`: an instrument, a scope of optional patchrig commits, scorer versions, vindex pins, and larql versions, a citation of one affected verdict event, and a reason.
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

The system SHALL provide `project_verdicts(events)`, a pure projection over events in global-log order. It SHALL read only event types and data, never parse stream ids, and ignore event types it does not own. It SHALL fold verdicts per (cell id, attempt, pre-registration), and never across attempts or pre-registrations. Within one group, a verdict whose `supersedes` names another verdict stream in the same group SHALL remove it permanently. A supersession cycle SHALL remove every verdict in it and be reported. After supersession, an invalidation SHALL remove every remaining verdict it cites, and every remaining verdict that matches its scope. Every present, non-empty scope list must match: patchrig commits against the measurement's patchrig commit, scorer versions against the verdict's scorer version, vindex pins against the measurement's vindex pin, and larql versions against the measurement's larql version. An invalidation SHALL apply only while no retraction cites its stream. Each group SHALL have exactly one status: `current` with exactly one verdict; `conflicting` with its candidates and a finding; `invalidated` when no verdict remains and an invalidation removed at least one; or `unresolved` when no verdict remains and none was removed by an invalidation. The projection SHALL NOT break ties, interpret detail, measurements, or the manipulation check, order dates, or consult a clock.

#### Scenario: A re-score supersedes the original

- **GIVEN** a measurement, a verdict on it, and a second verdict for the same cell and pre-registration whose `supersedes` names the first verdict's stream
- **WHEN** the events are projected
- **THEN** the group is `current` with the second verdict, citing its source event and the measurement

#### Scenario: Pre-registrations and attempts never fold together

- **GIVEN** two unsuperseded verdicts for one cell under two different pre-registrations
- **AND** two unsuperseded verdicts for one cell and pre-registration from attempts 1 and 2
- **WHEN** the events are projected
- **THEN** each pre-registration and each attempt has its own `current` group
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

#### Scenario: Scorer and measuring commits match separately

- **GIVEN** verdicts scored at commit `X`, re-scored at commit `Y` with `supersedes`, on measurements taken at patchrig commit `X`
- **AND** an invalidation whose scope is `scorerVersions: [X]`
- **WHEN** the events are projected
- **THEN** the re-scored verdicts are `current`
- **AND** an invalidation whose scope is `patchrigCommits: [X]` would remove them, because it names the measuring commit

#### Scenario: A superseded verdict does not return

- **GIVEN** verdict B supersedes verdict A in one group, and an invalidation then removes B
- **WHEN** the events are projected
- **THEN** the group is `invalidated` with no current verdict, and A does not return
- **AND** after a retraction of that invalidation, B is current again

#### Scenario: A group with no candidates and no invalidation is unresolved

- **GIVEN** a group whose verdicts all cite measurements absent from the log, or supersede each other in a cycle
- **WHEN** the events are projected
- **THEN** the group's status is `unresolved`, with no current verdict
- **AND** `verdict.unknown_measurement` or `verdict.supersedes_cycle` findings address its verdicts

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
- **THEN** each result serializes identically, groups are sorted by cell id, attempt, and pre-registration, and the input events are unchanged
