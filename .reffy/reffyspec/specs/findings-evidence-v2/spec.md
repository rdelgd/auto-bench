# findings-evidence-v2 Specification

## Purpose
Define version 2 of `evidence.recorded` and `verdict.recorded` for findings measured through hosted adapters, with one verdict per claim, adapter-scoped invalidations, and the projection of version 1 cells and version 2 runs side by side without either version reaching the other's fields.

## Requirements

### Requirement: Version 2 Evidence and Verdict Data

The system SHALL define version 2 data schemas for `evidence.recorded` and `verdict.recorded`, beside their unchanged version 1 schemas.

Version 2 `evidence.recorded` SHALL carry:
- a run id, an attempt, and a run kind;
- a records digest, a patchrig commit, and a claim scope;
- an adapter identity of kind, model, host, served date, and an optional route;
- a list of measurement items, whose `carrier` (string) and `tunedThreshold` (number) are typed when present, with other keys left free-form;
- optional inputs, fixture, pre-registration, and tier.

Version 2 `verdict.recorded` SHALL carry:
- a run id, an attempt, a claim id, and a claim;
- a citation of one measurement event, a pre-registration, a scorer version, and a verdict;
- optionally: a superseded verdict stream, a cannot-tell reason, detail, predicted verdict values, free-form statistics, and a policy event citation.

The four verdict values and the rule that a `cannotTellReason` is required with `cannot-tell` and forbidden otherwise SHALL apply to version 2 as to version 1. In version 2, `patchrigCommit` and `scorerVersion` SHALL be exactly 40 characters long, and every `served` date exactly 10, in both the adapter identity and adapter scope entries. The `verdict.invalidated` scope SHALL accept an optional `adapters` list within version 1. The checked-in schemas, the pure validator, and `jsonschema` SHALL agree.

#### Scenario: Validate the two-step finding

- **GIVEN** patchrig's two confirmation-run measurements and four claim verdicts for the two-step finding, with full commit hashes, event-reference citations, and predictions as lists of verdict values
- **WHEN** each is validated as version 2 data
- **THEN** every event is valid
- **AND** the same data is rejected as version 1

#### Scenario: Reject short hashes and unpadded dates

- **GIVEN** version 2 data with a 12-character `patchrigCommit`, a `scorerVersion` of `two-step@ec8e708727c6`, or a `served` date of `2026-11-4`
- **WHEN** it is validated
- **THEN** it is rejected with a structured finding at that field
- **AND** version 1 data with a short `scorerVersion` is still accepted, as in 0.5.0

#### Scenario: Keep named fields strict and free-form fields open

- **GIVEN** version 2 data
- **WHEN** it carries an unknown top-level key, a non-numeric `tunedThreshold`, a `predicted` given as text, or no `claimId`
- **THEN** it is rejected with a structured finding
- **AND** arbitrary keys inside `statistics`, `fixture`, or a measurement item are accepted

#### Scenario: Read version 1 unchanged

- **GIVEN** any version 1 event that `lasm-core` 0.5.0 accepts
- **WHEN** it is validated and projected by this version
- **THEN** its findings and its projected cell are identical to 0.5.0's

### Requirement: Projection Across Versions

`project_verdicts` SHALL project version 1 verdicts into `cells`, grouped per (cell id, attempt, pre-registration), and version 2 verdicts into `runs`, grouped per (run id, attempt, claim id, pre-registration). Both SHALL use the same supersession, invalidation, retraction, status, and finding rules. Groups of different versions SHALL never meet. A verdict citing a measurement of the other version SHALL be reported and SHALL NOT be a candidate. A scope list SHALL match only measurements that carry its field: version 1 pins never match version 2 measurements, and `adapters` never matches version 1 measurements, while patchrig commits and scorer versions apply to both. An adapter entry SHALL match when every field it gives equals the measurement's adapter identity. Dates SHALL be compared only for equality.

#### Scenario: Project the two-step finding

- **GIVEN** the two measurements and four verdicts of the two-step finding
- **WHEN** they are projected
- **THEN** `runs` holds four `current` groups, one per claim, each citing its run's measurement and carrying its adapter identity
- **AND** there are no findings and no conflicts

#### Scenario: Invalidate findings through one adapter

- **GIVEN** findings for `typesafe-ai/jev` through `ai-gateway.vercel.sh` and for `gpt-6-luna` through `api.openai.com`
- **AND** an invalidation whose `adapters` list names model `typesafe-ai/jev` and host `ai-gateway.vercel.sh`
- **WHEN** the events are projected
- **THEN** every Jev group through that gateway is `invalidated`, and every Luna group is unaffected
- **AND** an entry that also gives a `served` date reaches only findings served on that date

#### Scenario: Keep the versions apart

- **GIVEN** a log with version 1 cells and version 2 runs
- **WHEN** an invalidation names only a larql version, or only an adapter
- **THEN** the larql invalidation affects no run, and the adapter invalidation affects no cell
- **AND** an invalidation naming a patchrig commit or scorer version reaches both versions
- **AND** a version 2 verdict citing a version 1 measurement is reported as `verdict.measurement_version_mismatch`
