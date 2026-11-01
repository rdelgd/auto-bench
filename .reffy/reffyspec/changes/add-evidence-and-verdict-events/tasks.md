## 0. Before Implementation

- [x] 0.1 Get patchrig's answer on `patchrigCommit` and `larqlVersion` (names, and whether the run directory records both). Get their answers to open questions 2 and 3. Update the design with the answers.
- [x] 0.2 Get LogicalAssembly's review of the design, as with 0.4.0.
- [x] 0.3 Get patchrig's answer on renaming the measurement's `scope` (for example `claimScope`), or proceed with `scope`. Renamed to `claimScope`.

## 1. Checker and Schemas

- [x] 1.1 Add `else` and `not` to the shared checker in `_json_schema.py`. Confirm the interchange and parity suites pass unchanged, and the v1 schema files stay byte-identical.
- [x] 1.2 Add version 1 data schemas for `evidence.recorded`, `verdict.recorded`, `verdict.invalidated`, and `invalidation.retracted` to `_schema_ledger.py`, including the conditional `cannotTellReason` rule. Render them into `schemas/ledger/`.
- [x] 1.3 Extend `LedgerEventType` and `LEDGER_EVENT_TYPES`. Confirm `LEDGER_EVENT_SCHEMA_VERSIONS` and `validate_ledger_event_data` cover the new types. Add `verdict.reason_required` and `verdict.reason_not_allowed` as addressed findings.

## 2. Projection

- [x] 2.1 Add `src/lasm_core/verdict.py`: the records and literals, `VERDICT_VALUES`, `CANNOT_TELL_REASONS`, and `project_verdicts`.
- [x] 2.2 Implement indexing per (`cellId`, `attempt`, `preregistration`), then permanent supersession, then invalidation by citation and by condition with four scope lists, then retraction, then the four statuses.
- [x] 2.3 Implement the findings:
  - `verdict.conflict`
  - `verdict.supersedes_cycle`
  - `verdict.invalid_supersedes`
  - `verdict.unknown_measurement`
  - `invalidation.inconsistent_condition`
  - `invalidation.empty_scope`
  - `invalidation.cited_outside_scope`
  - `retraction.unknown_invalidation`
  - `ledger.unsupported_event`
  - `ledger.invalid_event_data`

## 3. Tests

- [x] 3.1 Schema tests: the checked-in files equal the rendered definitions. The pure validator and `jsonschema` agree on valid and invalid data for each new type, including:
  - each verdict value;
  - each reason code;
  - a reason missing with `cannot-tell`;
  - a reason present on another verdict;
  - an unknown reason code;
  - `null` for `supersedes`.
- [x] 3.2 Checker tests for `else` and `not`, nested and at the root, agreeing with `jsonschema`.
- [x] 3.3 Projection tests:
  - a single verdict is current;
  - a re-score supersedes;
  - invalid supersession;
  - two unsuperseded verdicts conflict;
  - separate pre-registrations and separate attempts never fold together;
  - a supersession cycle, including a self-supersession, is `unresolved` with a finding;
  - only unknown measurements is `unresolved`;
  - a superseded verdict stays gone when its replacement is invalidated, and the replacement returns on retraction;
  - `scorerVersions` spares re-scored verdicts that `patchrigCommits` would remove;
  - invalidation by citation;
  - invalidation by condition, including a verdict written after the invalidation;
  - multi-list scope matching;
  - empty scope;
  - an inconsistent condition;
  - a citation outside the scope;
  - a retraction restores verdicts;
  - a retraction of an unknown invalidation;
  - a dangling measurement;
  - unreadable events;
  - foreign types ignored;
  - deterministic, sorted, non-mutating output.
- [x] 3.4 Extend `tests/test_sans_io.py` to cover `project_verdicts`. Add the new callables to the `POST_MIGRATION` allowlist.

## 4. Package and Documentation

- [x] 4.1 Export the new API from `lasm_core`, and bump to `0.5.0`. Confirm the wheel includes the four new schema files.
- [x] 4.2 Update `docs/api-inventory.md`, `README.md`, and `.reffy/reffyspec/project.md`.
- [x] 4.3 Run `uv run pytest` on the development and minimum interpreters, `uv run mypy`, `scripts/write_schemas.py --check`, and a wheel build.
- [x] 4.4 Run `reffy plan validate add-evidence-and-verdict-events` and `reffy validate`.
- [ ] 4.5 Tag `v0.5.0`, and tell LogicalAssembly, patchrig, and Rastro.
- [ ] 4.6 Archive the change.
