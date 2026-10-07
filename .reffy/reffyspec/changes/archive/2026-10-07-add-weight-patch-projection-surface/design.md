## Context

`lasm_core` is a Sans I/O Python library. Projection surfaces are `TypedDict` descriptors with camelCase wire keys, each carrying an optional `LasmProjectionReferences`. The evaluator reads those references for reality coverage, reads trace events to decide whether expected surfaces were used, and attributes findings to one of six `DivergenceSource` values. The version 1 interchange schemas are rendered from `_schema_v1.py`, and a TypeScript-era corpus under `tests/corpus/reference/` is matched by `tests/test_parity.py` after reviewed deviations.

The collective-mind artifact asks for a weight-patch projection surface so that a compiled knowledge patch can be modeled, expected, observed, and blamed the same way a skill or MCP surface can. The binding-record artifact supplies the scope test: keep in the core what survives a platform migration, needs an accountable person, or is needed to attribute a divergence. The descriptor passes. Patch compilation, serving, and probing do not.

## Goals / Non-Goals

Goals:

- Model a weight patch as a first-class Lasm projection with a digest and a required projection claim.
- Let a scenario expect a patch and let a trace show one being applied and probed.
- Let Auto Bench report an unmodeled, unused, digest-mismatched, or probe-failing patch, and name the patch when a projected entry diverges.
- Keep every existing case, document, fixture, and recorded evaluation unchanged.
- Add a reference fixture that exercises the new findings end to end without any live system.

Non-goals:

- A `BindingEntry` record or any entry-to-implementation mapping beyond the descriptor's own projection claim.
- New `DivergenceSource` values, new evaluation dimensions, or a `fidelity` vocabulary.
- Representing probe kinds, patch methods, training data, or rig configuration in the core.
- Changing `ProvenanceStatus`, the service-scheduling fixture, or the recorded corpus inputs.
- Any adapter to the in-vitro-patching rig, a model server, or Databricks.

## Decisions

### 1. One thin descriptor, projection required

```
WeightPatchDescriptor
  id: str
  name: str
  purpose: str
  baseModelId: str          # the model or trunk the patch is applied to
  digest: str               # content digest of the compiled patch
  projection: LasmProjectionReferences
```

`projection` is required, unlike the other descriptors where it is optional. A harness or MCP server can exist without projecting Lasm meaning. A weight patch in a conformance case exists only because it claims to carry meaning; a patch with no claim is not a Lasm projection and should not be in the case. Validation reuses `projection.empty` and the unknown-reference codes.

`baseModelId` and `digest` are plain strings. The core does not compute digests, compare models, or know what a patch method is. They are the fields a later binding record would reference.

Module: `src/lasm_core/weight_patch.py`. Exports: `WeightPatchDescriptor`, `validate_weight_patch`.

### 2. Optional collections, omitted means empty

`ConformanceCase` gains `weightPatches: NotRequired[Sequence[WeightPatchDescriptor]]` and `ExpectedControlSurfaces` gains `weightPatchIds: NotRequired[Sequence[str]]`. Both are read with `.get(..., [])`.

This is the first optional collection on either record. The reason is compatibility: every recorded corpus input, the service-scheduling fixture, and every version 1 document already in circulation lacks these keys. Making them required would force a schema version bump and a fixture-content deviation for a purely additive feature. The cost is one `.get` in each reader.

### 3. Two events, minimal evidence contract

Added to `AgenticEventType` after the `mcp.*` group:

| Event | `subjectId` | Evidence read by the evaluator |
| --- | --- | --- |
| `patch.applied` | weight patch id | `digest` (string) |
| `patch.probed` | weight patch id | `probe` (string label), `passed` (boolean) |

Evidence stays an open `EvidencePayload`. The rig may record probe kind, target entry, neighbour and far-field scores, or anything else; the evaluator reads only `digest`, `probe`, and `passed`. A `patch.probed` event whose `passed` is absent or not a boolean is treated as not passed, matching the project rule that an unverified claim is not evidence of success.

### 4. Evaluation changes, by dimension

| Dimension | Change |
| --- | --- |
| reality-coverage | `_projection_references` includes each weight patch's projection, so an entry projected only by a patch is covered. |
| control-surface-quality | A fifth check row: expected `weightPatchIds` against fixture ids and `patch.applied` subjects. New codes `control.weight_patch_fixture_missing`, `control.weight_patch_not_used`, `control.weight_patch_unmodeled`. Then, for every `patch.applied` whose subject is a modeled patch, `control.weight_patch_digest_mismatch` (error, `control-surface`) when evidence `digest` differs from the descriptor's. Then, for every `patch.probed` on a modeled patch that did not pass, `control.weight_patch_probe_failed` (error, `projection`) addressing the patch's projected entry ids. |
| semantic-fidelity | After the existing `semantic.divergence_detected` finding, if the divergence subject is projected by one or more weight patches, add `semantic.divergence_in_weight_patch` (error, `projection`) whose message names the patch ids. |

The digest check lives in control-surface-quality rather than reality-model-validity because the assembly is not wrong; the deployed surface is not the approved one. The probe failure is attributed to `projection` because the patch failed to carry meaning it claimed, which is what the existing `projection` value means.

`EvaluationFinding` is unchanged. Naming the patch in the message rather than in a new `projectionIds` field keeps the result schema and all recorded evaluations stable. A general surface-id field on findings is a reasonable follow-on but widens this change into the result contract.

With no weight patches and no patch events, every existing dimension produces exactly its current findings, including the `control.expected_surfaces_used` passing finding whose expected-id list grows by nothing.

### 5. Validation

`validate_weight_patch(patch, assembly=None, state=None)` follows `validate_skill`: required `id`, `name`, `purpose`, `baseModelId`, `digest`; projection references validated against the assembly and state when supplied. Paths use the `weightPatch.` prefix.

`validate_conformance_case` adds, in order: per-patch validation after MCP surfaces; `scenario.unknown_weight_patch` for expected ids with no fixture; and `_unique_ids` over `weightPatches` after `mcpSurfaces`. `validate_scenario` includes `weightPatchIds` in the uniqueness check over expected control surfaces.

### 6. Interchange

Add `WeightPatchDescriptor` to `DEFINITIONS`. Add the two optional properties. Extend the `AgenticEventType` enum, which is derived from the trace module and so changes automatically. Re-render `schemas/v1/` with `scripts/write_schemas.py`. `schemaVersion` stays 1 because the change is additive and omitted fields keep their current meaning.

### 7. Second reference fixture

`src/lasm_core/fixtures/new_vehicle_units.py`, domain `sales`. One assembly with a `net new-vehicle units` concept, a `stock type` concept, a relation between them, a policy naming the accountable owner, and a check-mode runtime evaluation. One weight patch claiming both concepts. One skill claiming the same. A scenario expecting the skill and the patch. A trace in which the patch is applied with the correct digest, a `canonical` probe passes, a `paraphrase` probe fails, the agent answers with a retail-only count, a prohibited outcome is observed, and a divergence is detected on the units concept and attributed.

The recorded evaluation is nonconformant with findings in control-surface-quality (`control.weight_patch_probe_failed`), semantic-fidelity (`semantic.divergence_in_weight_patch` naming the patch), and state-and-outcome-validity (`outcome.prohibited_observed`). This is the collective-mind artifact's "attributed from the control plane" probe, with a fake digest and no rig.

The service-scheduling fixture is not modified. Its recorded corpus entries remain byte-identical.

### 8. Parity and coverage

- `tests/corpus/deviations.json` gains one entry for the `agenticEventTypes` constant case, with this change id and the reason that two event types were added after migration.
- `test_corpus_covers_every_public_behavioral_export` currently requires every public callable to be in the TypeScript corpus. That test gains an explicit `POST_MIGRATION` allowlist, alongside the existing `interchange` set, naming `validate_weight_patch`. Post-migration exports are covered by ordinary pytest tests. The corpus is never regenerated from Python.
- The new fixture's exports are not added to `FIXTURES` in `corpus_support.py`, because that mapping is the TypeScript-era fixture set. They are covered by a new fixture test that validates and evaluates the case and asserts the recorded evaluation.

### 9. Package

Version `0.3.0`. `__init__.py` exports the new type and validator. `docs/api-inventory.md` gains an "Added after migration" section listing `WeightPatchDescriptor`, `validate_weight_patch`, and the new fixture exports, so `test_api_inventory_documents_every_public_symbol` passes. README and `project.md` list weight patches among projection surfaces and the new events among evidence.

## Risks

- **Scope creep toward the rig.** The temptation is to put probe kinds or patch methods in the descriptor. The scope test says no: those do not survive a platform migration and are not needed for attribution. If a future case needs them, they belong in evidence payloads.
- **Reading `passed` leniently.** Treating a missing boolean as failure may surprise an adapter that records probes without a verdict. That is the intended behavior and is documented in the event contract.
- **Schema consumers.** Any external decoder pinned to the old `domain.schema.json` will reject documents that use the new fields. No such consumer is known. The interchange requirement already allows additive version 1 changes.

## Open Questions

1. Should a `patch.applied` event for a patch that is modeled but not expected be a warning rather than an error? The existing `control.*_unmodeled` codes are errors only when the surface is absent from the fixture, so an applied, modeled, unexpected patch currently produces no finding. This change keeps that behavior for consistency.
2. Does `baseModelId` need to be cross-checked against anything in the case? Nothing else in `lasm_core` names a model today. It is recorded, not validated.
3. When a `BindingEntry` arrives, should `WeightPatchDescriptor.projection` become derived from accepted bindings rather than asserted on the descriptor? That is a question for the binding change, not this one.
