## 1. Records and Schemas

- [x] 1.1 Move the structural JSON Schema checker out of `interchange.py` into a private shared module with no behavior change. Confirm the interchange and parity suites pass unchanged.
- [x] 1.2 Add `src/lasm_core/ledger.py` with `LedgerEventType`, `PolicyDecision`, `LedgerEventRef`, `PolicyAcceptedData`, `DecisionMadeData`, `RemovalApproval`, `ApplicationRemovedData`, `NewEvent`, `RecordedEvent`, `AcceptPolicy`, `PolicyCommandResult`, `DecisionRuleRecord`, `DecisionRuleProjection`, `FIRST_SLICE_BINDINGS`, `LEDGER_EVENT_SCHEMA_VERSIONS`, `policy_stream_id`, and `application_stream_id`.
- [x] 1.3 Add `src/lasm_core/_schema_ledger.py` with version 1 data schemas for the three event types. Extend `scripts/write_schemas.py` to render `src/lasm_core/schemas/ledger/` and to cover it in `--check`.
- [x] 1.4 Add `validate_ledger_event_data(type, schema_version, data)` using the shared checker, plus `ledger.unsupported_event`.

## 2. Aggregate and Projection

- [x] 2.1 Implement `decide_policy` with the rejection codes `policy.invalid_binding`, `policy.invalid_action`, `policy.id_mismatch`, `fixture.required`, `policy.reason_required`, `policy.unchanged`, and `policy.unsupported_event`. Report every applicable rejection, not just the first.
- [x] 2.2 Implement `project_decision_rules`: fold in the given order, latest acceptance wins per (binding, action), cite the source event, ignore foreign types, report `ledger.unsupported_event` and `ledger.invalid_event_data`, and sort the rules by (binding, action).

## 3. Tests

- [x] 3.1 Schema tests: checked-in files equal the rendered definitions; the pure validator and `jsonschema` agree on valid and invalid data for each type.
- [x] 3.2 Aggregate tests: accept, each rejection, idempotent re-acceptance, changed-content re-acceptance, an unsupported past event, and no input mutation.
- [x] 3.3 Projection tests: fold order, latest acceptance wins, citations, foreign types ignored, invalid-event findings, replay from empty equals incremental replay, and repeatable sorted output.
- [x] 3.4 End-to-end test: seed the three paseo-core rules through `decide_policy`, project them, and get exactly the seed rules.
- [x] 3.5 Extend `tests/test_sans_io.py` to cover the ledger functions. Add them to the `POST_MIGRATION` allowlist in the parity coverage test.

## 4. Package and Documentation

- [x] 4.1 Export the ledger API from `lasm_core.__init__`. Bump `__version__` and `pyproject.toml` to `0.4.0`. Confirm the wheel includes `schemas/ledger/`.
- [x] 4.2 Add the ledger API to `docs/api-inventory.md` under "Added after migration". Confirm `test_api_inventory_documents_every_public_symbol` passes.
- [x] 4.3 Update `README.md` and `.reffy/reffyspec/project.md`: ledger semantics, the separate schema line, and the git-tag distribution for LogicalAssembly.
- [x] 4.4 Run `uv run pytest`, `uv run mypy`, `uv run python scripts/write_schemas.py --check`, and a wheel build.
- [x] 4.5 Run `reffy plan validate add-world-ledger-governance-events` and `reffy validate`.
- [x] 4.6 Tag `v0.4.0` and reply to LogicalAssembly with the pin and the answers to their four questions.
- [x] 4.7 Archive the change.
