## 0. Before Implementation

- [x] 0.1 Get patchrig's agreement to the five points in `lasm-core-reply-on-findings-event-data.md`:
  - full commit hashes;
  - `cites` as an event reference;
  - `predicted` as a list;
  - the verdict's numbers in `statistics`;
  - adapter matching by equality.
- [x] 0.2 Get LogicalAssembly's review of the design. Accepted; exact lengths adopted from its suggestion.

## 1. Schemas

- [x] 1.1 Add `evidence.recorded` version 2 and `verdict.recorded` version 2 to `_schema_ledger.py`, including the open `MeasurementItem` and the conditional `cannotTellReason` rule. Render both into `schemas/ledger/`.
- [x] 1.2 Add the optional `adapters` list to `verdict.invalidated` version 1's scope. Re-render the file. Confirm every other existing schema file is byte-identical.
- [x] 1.3 Confirm `LEDGER_EVENT_SCHEMA_VERSIONS` reports `(1, 2)` for both types, and that `validate_ledger_event_data` covers version 2, including the addressed reason findings.

## 2. Projection

- [x] 2.1 Add the version 2 records to `verdict.py`. Add `runs` to `VerdictProjection`.
- [x] 2.2 Group version 2 verdicts per (`runId`, `attempt`, `claimId`, `preregistration`), keyed apart from version 1 groups. Share the resolution with version 1.
- [x] 2.3 Implement cross-version matching: `adapters` against the version 2 `adapter`, version 1 lists never matching version 2, and `adapters` never matching version 1.
- [x] 2.4 Report `verdict.measurement_version_mismatch` for a verdict citing the other version's measurement.

## 3. Tests

- [x] 3.1 Schema tests: the pure validator and `jsonschema` agree on patchrig's draft data, corrected per the reply, and on invalid variants:
  - a missing `claimId` or `adapter`;
  - `predicted` as text;
  - an unknown key at the top level, but not inside `statistics` or a measurement item;
  - a non-numeric `tunedThreshold`;
  - the reason rule.
- [x] 3.2 The two-step finding end to end: two measurements and four verdicts project as four `current` run groups, with no findings.
- [x] 3.3 Cross-version tests:
  - v1 and v2 events in one log project into `cells` and `runs` independently;
  - a larql invalidation spares v2 findings;
  - an adapter invalidation spares v1 cells;
  - `patchrigCommits` and `scorerVersions` reach both versions;
  - cross-version `supersedes` and `cites` are reported.
- [x] 3.4 Adapter matching: by model and host; narrowed by `served` and `route`; several entries; a different gateway is not matched.
- [x] 3.5 Every 0.5.0 projection test still passes, with `runs` empty. Extend the Sans I/O test to cover a version 2 log.

## 4. Package and Documentation

- [x] 4.1 Export the new records, and bump to `0.6.0`. Confirm the wheel includes the new schema files.
- [x] 4.2 Update `docs/api-inventory.md`, `README.md`, and `.reffy/reffyspec/project.md`.
- [x] 4.3 Run `uv run pytest` on both interpreters, `uv run mypy`, `scripts/write_schemas.py --check`, and a wheel build.
- [x] 4.4 Run `reffy plan validate add-findings-evidence-v2` and `reffy validate`.
- [x] 4.5 Tag `v0.6.0`, and tell LogicalAssembly, patchrig, and Rastro.
- [ ] 4.6 Archive the change.
