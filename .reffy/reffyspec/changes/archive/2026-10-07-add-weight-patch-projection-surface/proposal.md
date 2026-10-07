# Change: Add Weight-Patch Projection Surface to lasm_core

## Why

`lasm_core` models three kinds of agent-facing projection: harness context, skills, and MCP surfaces. Each carries `LasmProjectionReferences` that say which assembly entries and state fields it claims to expose. Auto Bench uses those claims to decide whether relevant meaning was projected at all, whether the expected surface was used, and whether a divergence belongs to a projection or to agent conduct.

The in-vitro-patching work in the `lasm-v1` workspace adds a fourth kind of surface: a compiled knowledge patch written into the weights of a model the fleet owns. The collective-mind artifact argues that such a patch is the same kind of thing as a skill or an MCP surface. It claims to realize certain entries. It has a version. It can be lossy. It can be the place a wrong meaning came from. Today `lasm_core` cannot say any of that, so a patch-caused divergence is argued about beside the evaluator rather than attributed by it.

This change gives `lasm_core` a seventh projection surface, `WeightPatchDescriptor`, with the evidence events and evaluation checks needed to treat a patch as a Lasm projection. It is deliberately small: a capability family added alongside existing descriptors, not a new kind of actor, record, or evaluation dimension.

## What Changes

- Add `WeightPatchDescriptor` to `lasm_core`: a projection surface identified by a stable id, the base model it patches, a content digest, and a required `LasmProjectionReferences`.
- Add an optional `weightPatches` collection to `ConformanceCase` and an optional `weightPatchIds` list to `ExpectedControlSurfaces`. Both are omitted-means-empty so every existing version 1 document remains valid.
- Add two evidence event types, `patch.applied` and `patch.probed`, to the agentic trace vocabulary.
- Add `validate_weight_patch` and extend conformance-case validation with weight-patch id uniqueness and expected-id resolution.
- Extend evaluation so that reality coverage counts weight-patch projections, control-surface quality checks expected and unmodeled patches, an applied patch whose digest differs from its descriptor is a control-surface finding, a failed probe is a projection finding, and a semantic divergence on an entry projected by a patch names that patch.
- Add the `WeightPatchDescriptor` record and the two new fields to the version 1 interchange schemas as additive optional content. The format version stays at 1.
- Add a second automotive reference fixture, a sales-domain new-vehicle-units episode in which a patch carries a KPI definition and a paraphrase probe reveals it dropped the stock-type distinction.
- Record one parity deviation for the event-type constant and allow post-migration exports to be covered by ordinary tests rather than the TypeScript corpus.
- Bump the package to `0.3.0` and update the API inventory, README, and project context.

## Impact

- Affected capability: `establish-auto-bench-sans-io-core`. No new capability is introduced.
- Affected implementation: `src/lasm_core/weight_patch.py` (new), `conformance.py`, `scenario.py`, `trace.py`, `validate.py`, `evaluate.py`, `_schema_v1.py`, `__init__.py`, `fixtures/`, rendered schemas under `schemas/v1/`, `tests/`, `tests/corpus/deviations.json`, `docs/api-inventory.md`, `README.md`, `.reffy/reffyspec/project.md`.
- Compatibility: additive. Existing typed callers, fixtures, and version 1 documents are unaffected. Decoders built from the previous schema set will reject documents that use the new optional fields, which is the normal consequence of `additionalProperties: false` and is accepted.
- Parity: evaluation outputs for the recorded corpus are unchanged because no recorded case has weight patches or patch events. The `agenticEventTypes` constant case changes and is recorded as a reviewed deviation.
- Out of scope: a `BindingEntry` record, changes to `ProvenanceStatus`, a new `DivergenceSource` value, a new evaluation dimension, a `fidelity` vocabulary, any patch compilation, serving, or probing mechanics, and any connection to the in-vitro-patching rig. The descriptor's `digest` and `baseModelId` are the fields a later binding record would point at.

## Supersedes

None

## Reffy References

- `lasm-as-the-collective-mind-control-plane.md` - the weights as a projection target; the concrete next step this change implements; probes as conformance evidence rather than descriptor fields
- `lasm-binding-record-as-the-sovereign-unit.md` - the scope test used to keep the descriptor in the core and the rig in adapters; the digest as what makes "evaluated, approved, released, and used" checkable; the new-vehicle-units probe the second fixture is modeled on
- `lasm-as-sovereign-mapping-plugin.md` - the keep-versus-adapter table; the rule that a Lasm evaluation descriptor states what must be checked while a native runner executes it
