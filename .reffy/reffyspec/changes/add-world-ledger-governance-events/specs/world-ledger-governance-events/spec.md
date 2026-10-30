## ADDED Requirements

### Requirement: Ledger Event Semantics in the Core

The system SHALL own the meaning of world-ledger events in `lasm_core`: event types, the schemas of their `data`, the aggregates that decide which events may be appended, and the projections folded from them. It SHALL NOT own ledger storage, ordering, durability, idempotency, attribution, event ids, polling, or the ledger envelope beyond a `RecordedEvent` view of stream id, stream version, type, schema version, and data. All ledger functions SHALL be Sans I/O, deterministic, and non-mutating, and SHALL consult no clock.

#### Scenario: Use ledger semantics without I/O

- **GIVEN** ledger events materialized as `RecordedEvent` values and a command materialized as a typed value
- **WHEN** a consumer invokes the ledger aggregate, projection, or data validator
- **THEN** each returns a structured value
- **AND** it performs no file, environment, network, process, database, or clock access
- **AND** the caller's events and command are unchanged

### Requirement: Governance Event Types

The system SHALL define three version 1 ledger event types with camelCase `data` records: `policy.accepted` on stream `policy:<policyId>` (policy id, binding, action, decision, a reason, and the accepter); `decision.made` on stream `application:<applicationId>` (decision id, application id, action, the resource object, requester, request time, decision, a required basis of `rule`, `unknown-action`, `unknown-application`, or `no-rule`, an optional reason, an optional citation of the policy event by stream id and version, an optional projection position, and an optional trace id); and `application.removed` on stream `application:<applicationId>` (application id, removal time, an optional remover, an optional approval whose decision id, bypassed flag, and required flag are each optional, and whether the application was registered). Provenance that the source did not report SHALL be omitted rather than invented. Event-time fields SHALL be carried as data and never derived from ledger order. Each event type SHALL be versioned independently of the others and of interchange version 1. Its schema SHALL be rendered under `schemas/ledger/` and checked by a pure validator that agrees with `jsonschema`.

#### Scenario: Validate event data against its schema

- **GIVEN** data for a known event type and schema version
- **WHEN** `validate_ledger_event_data` runs
- **THEN** well-formed data produces no findings
- **AND** a missing required field, an unknown property, or a wrong scalar type produces a structured format finding
- **AND** `jsonschema` with the checked-in schema reaches the same accept or reject verdict

#### Scenario: Reject an unknown type or version

- **GIVEN** data labeled with an event type or schema version this release does not define
- **WHEN** `validate_ledger_event_data` runs
- **THEN** it reports `ledger.unsupported_event` and accepts nothing

#### Scenario: Backfill a historical decision without a policy citation

- **GIVEN** a historical fail-closed denial with no accepted policy behind it and no projection position
- **WHEN** it is recorded as `decision.made` data with basis `no-rule` that omits `policy`, `projectionPosition`, and `traceId`
- **THEN** the data is valid
- **AND** data without a `basis`, with an unknown basis, with a string `resource`, or with a `bypassed` field is rejected

#### Scenario: Backfill a removal without reported provenance

- **GIVEN** a historical removal whose remover is empty and whose approval reported nothing
- **WHEN** it is recorded as `application.removed` data that omits `removedBy` and `approval`
- **THEN** the data is valid
- **AND** an `approval` that carries only `bypassed` is also valid

### Requirement: Policy Acceptance Aggregate

The system SHALL provide `decide_policy(past_events, command)`. Given the events of one policy stream and an `AcceptPolicy` command, it SHALL return either exactly one `policy.accepted` event to append or one or more rejection findings. It SHALL reject an unknown binding, an action not belonging to the binding, a policy id other than `<binding>.<action>`, a blank accepter, a `deny` without a non-blank reason, content identical to the stream's latest accepted binding, action, decision, and reason, and any past event whose type, schema version, or data it does not understand. A command that does not match the `policy.accepted` version 1 data shape SHALL be rejected with structured format findings. The first-slice binding SHALL be `paseo-core`, with actions `application.teardown`, `agent.retire`, and `workspace.delete`.

#### Scenario: Accept a policy onto an empty stream

- **GIVEN** no past events and a command to deny `application.teardown` under `paseo-core`, with policy id `paseo-core.application.teardown`, a reason, and an accepter
- **WHEN** `decide_policy` runs
- **THEN** it is accepted with one `policy.accepted` schema version 1 event whose data repeats the command
- **AND** it reports no findings

#### Scenario: Reject an invalid command

- **GIVEN** a command with an unknown binding, an unknown action, a mismatched policy id, a blank accepter, or a `deny` without a reason
- **WHEN** `decide_policy` runs
- **THEN** it is not accepted, produces no events, and reports each applicable rejection code

#### Scenario: Refuse a duplicate acceptance

- **GIVEN** a policy stream whose latest accepted content equals the command's binding, action, decision, and reason
- **WHEN** `decide_policy` runs, even with a different accepter
- **THEN** it reports `policy.unchanged` and produces no events
- **AND** a command that changes the decision or the reason is accepted

### Requirement: Decision Rule Projection

The system SHALL provide `project_decision_rules(events)`, which folds `policy.accepted` events in the given order into one rule per (binding, action), keeping the latest acceptance. Each rule SHALL carry the decision, any reason, the policy id, and a citation of the source event by stream id and stream version. Rules SHALL be returned sorted by binding and action. Events of other types SHALL be ignored. A `policy.accepted` event with an unsupported schema version or invalid data SHALL be skipped and reported as a finding. The projection SHALL NOT supply default rules for actions that have no accepted policy.

#### Scenario: Latest acceptance wins

- **GIVEN** two `policy.accepted` events for `paseo-core.workspace.delete`, the first allowing and the second denying with a reason
- **WHEN** the events are projected in ledger order
- **THEN** one rule for `workspace.delete` denies with that reason and cites the second event's stream id and version

#### Scenario: Replay is deterministic

- **GIVEN** the same sequence of recorded events, including events of types the projection does not own
- **WHEN** it is projected from empty more than once
- **THEN** each result serializes identically
- **AND** foreign event types do not affect the rules

#### Scenario: Report an event the projection cannot read

- **GIVEN** a `policy.accepted` event with an unknown schema version or data that fails validation
- **WHEN** the events are projected
- **THEN** that event contributes no rule
- **AND** the result carries a finding addressing the event's index so the adapter can refuse to rewrite its rule table

#### Scenario: Reproduce today's rules

- **GIVEN** the three current paseo-core decision rules seeded through `decide_policy` and recorded on their policy streams
- **WHEN** the recorded events are projected
- **THEN** the result has exactly three rules, equal to the seeded decisions and reasons
