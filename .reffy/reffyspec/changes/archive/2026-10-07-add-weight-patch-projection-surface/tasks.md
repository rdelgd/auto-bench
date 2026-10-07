## 1. Model the Surface

- [x] 1.1 Add `src/lasm_core/weight_patch.py` with `WeightPatchDescriptor` (`id`, `name`, `purpose`, `baseModelId`, `digest`, required `projection`) and `validate_weight_patch` following the `validate_skill` pattern with `weightPatch.` paths.
- [x] 1.2 Add `weightPatches` (optional) to `ConformanceCase` and `weightPatchIds` (optional) to `ExpectedControlSurfaces`; read both as empty when omitted.
- [x] 1.3 Add `patch.applied` and `patch.probed` to `AgenticEventType` after the `mcp.*` group; confirm `AGENTIC_EVENT_TYPES` and the schema enum pick them up.
- [x] 1.4 Export the new type and validator from `lasm_core.__init__` and bump `__version__` and `pyproject.toml` to `0.3.0`.

## 2. Validate and Evaluate

- [x] 2.1 Extend `validate_conformance_case`: per-patch validation after MCP surfaces, `scenario.unknown_weight_patch` for unresolved expected ids, and `_unique_ids` over `weightPatches`; include `weightPatchIds` in `validate_scenario`'s uniqueness check.
- [x] 2.2 Include weight-patch projections in `_projection_references` so reality coverage counts them.
- [x] 2.3 Add the weight-patch row to the control-surface checks with codes `control.weight_patch_fixture_missing`, `control.weight_patch_not_used`, and `control.weight_patch_unmodeled`.
- [x] 2.4 Add `control.weight_patch_digest_mismatch` (error, `control-surface`) for an applied modeled patch whose evidence `digest` differs from the descriptor.
- [x] 2.5 Add `control.weight_patch_probe_failed` (error, `projection`, addressing the patch's projected entry ids) for a `patch.probed` event on a modeled patch whose `passed` is not `true`.
- [x] 2.6 Add `semantic.divergence_in_weight_patch` (error, `projection`) after `semantic.divergence_detected` when the divergence subject is projected by one or more weight patches; name the patch ids in the message.
- [x] 2.7 Confirm by test that a case with no weight patches and no patch events produces findings identical to the current implementation.

## 3. Interchange

- [x] 3.1 Add `WeightPatchDescriptor` to `_schema_v1.DEFINITIONS`; add the optional `weightPatches` and `weightPatchIds` properties; keep `SCHEMA_VERSION` at 1.
- [x] 3.2 Re-render `src/lasm_core/schemas/v1/` with `scripts/write_schemas.py` and confirm `test_checked_in_schemas_are_rendered_from_the_python_definitions` passes.
- [x] 3.3 Add interchange tests: a case document with weight patches round-trips; a document omitting them decodes to the same payload as before; a patch without `projection` or with an unknown field is rejected structurally; an empty `projection` is admitted by the schema and reported by `validate_weight_patch`.

## 4. Reference Fixture

- [x] 4.1 Add `src/lasm_core/fixtures/new_vehicle_units.py` (domain `sales`) with the assembly, initial state, observations, transitions, outcomes, harness, skill, weight patch, scenario, trace, conformance case, and recorded evaluation described in the design.
- [x] 4.2 Export the fixture values from `lasm_core.fixtures` and confirm the core root import does not load the fixture module.
- [x] 4.3 Add a fixture test that validates the case with no findings, evaluates it, and asserts `conformant` is false with `control.weight_patch_probe_failed`, `semantic.divergence_in_weight_patch` naming the patch id, and `outcome.prohibited_observed` present and attributed as designed.
- [x] 4.4 Add a conformant variant in the test (correct digest, all probes passed, no divergence) and assert control-surface-quality and semantic-fidelity pass.

## 5. Parity, Coverage, and Sans I/O

- [x] 5.1 Add the `agenticEventTypes` deviation to `tests/corpus/deviations.json` under this change id with a reason naming the two added events; confirm `test_every_deviation_is_explained_and_changes_a_recorded_case` passes.
- [x] 5.2 Run the full parity suite and confirm every other recorded case, including all `evaluateConformance` and `fixtures` cases, matches without a deviation.
- [x] 5.3 Add a `POST_MIGRATION` allowlist to `test_corpus_covers_every_public_behavioral_export` containing `validate_weight_patch`; do not add new fixtures to `FIXTURES` in `corpus_support.py`.
- [x] 5.4 Add unit tests for `validate_weight_patch` (required fields, empty projection, unknown entry and state-field references) and for the new case-level codes.
- [x] 5.5 Extend the Sans I/O test to evaluate the new fixture with file, environment, network, process, and clock access patched to fail, and the repeatability test to cover it.

## 6. Documentation and Close

- [x] 6.1 Add an "Added after migration" section to `docs/api-inventory.md` listing `WeightPatchDescriptor`, `validate_weight_patch`, and every new fixture export; confirm `test_api_inventory_documents_every_public_symbol` passes.
- [x] 6.2 Update `README.md` ("What Exists Today" and the projection list) and `.reffy/reffyspec/project.md` (code-style names, architecture patterns, domain context) to include weight patches and the two events.
- [x] 6.3 Run `uv run pytest`, `uv run mypy`, and a wheel build; confirm all pass on the minimum and development interpreters.
- [x] 6.4 Run `reffy plan validate add-weight-patch-projection-surface` and `reffy validate`; resolve every finding.
- [ ] 6.5 Archive the change and apply the delta to `specs/establish-auto-bench-sans-io-core/spec.md`.
