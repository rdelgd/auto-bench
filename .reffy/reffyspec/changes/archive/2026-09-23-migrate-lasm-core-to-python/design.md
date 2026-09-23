## Context

`@lasm/core` is currently a small TypeScript library with explicit JSON-shaped domain types and pure functions. Its implementation spans assemblies, provenance, projections, operational state, scenarios, trace normalization, validation, and eight evaluation dimensions. The automotive service-scheduling fixture supplies a complete episode, and tests exercise both conformance and failures.

The proposed workbench introduces likely Python consumers around this core. Moving the implementation now can simplify those consumers while retaining the existing boundary: adapters materialize inputs and perform I/O; Lasm computes materialized results.

## Goals / Non-Goals

Goals:

- Provide one typed Python implementation of the complete current public domain API.
- Preserve validation, normalization, evaluation, and fixture behavior across the language change.
- Make the input/output contracts usable independently of Python or TypeScript.
- Preserve repeatability, caller-owned inputs, and isolation from live systems.
- Finish with a Python-only core development and execution path.

Non-goals:

- Expanding or redesigning the ontology, evaluation dimensions, or automotive scope.
- Fixing unrelated evaluator defects as part of the port or treating parity as proof that existing evaluation semantics are sufficient.
- Adding an agent framework, model-based judge, web service, CLI product, persistence layer, workbench UI, or platform integration.
- Maintaining two evaluators indefinitely, providing an npm compatibility shim, or implementing browser-side evaluation.
- Publishing packages to a public registry or changing archived planning history.

## Decisions

### 1. Python package and public surface

Use the distribution name `lasm-core` and import namespace `lasm_core`, with Python 3.11 as the minimum supported version. Declare the support range in `pyproject.toml`, test the minimum and the selected development interpreter, and provide wheel and source distributions. Registry availability is a separate concern if public publication is proposed later.

Use a `src/lasm_core/` package layout and a separate `lasm_core.fixtures` namespace. Preserve the complete public surface of the existing root and fixture exports through an explicit migration inventory, including the smaller helpers and individual validators. Representative mappings are:

| Current TypeScript surface | Python surface |
| --- | --- |
| `@lasm/core` | `lasm_core` |
| `@lasm/core/fixtures` | `lasm_core.fixtures` |
| `LogicalAssemblySlice`, `ConformanceCase`, `ConformanceEvaluation` | Same domain type names |
| `validateConformanceCase`, `validateLogicalAssembly` | `validate_conformance_case`, `validate_logical_assembly` |
| `normalizeTrace`, `traceEvidenceRef` | `normalize_trace`, `trace_evidence_ref` |
| `evaluateConformance` | `evaluate_conformance` |
| `routineMaintenanceConformanceCase` | `routine_maintenance_conformance_case` |

Use standard-library `TypedDict`, `Literal`, and collection types for JSON-shaped public records, with a `py.typed` marker and static checking. Record keys remain the existing camelCase wire names; Python function and module names use snake_case. This mirrors the existing TypeScript interface model without introducing an object-mapping framework or runtime coercion.

Document non-JSON helper return types in the migration inventory. In particular, the TypeScript `logicalAssemblyEntryIds` helper returns a set; its Python equivalent may return a `frozenset`. The compatibility promise for this helper is member identity, while ordered domain arrays and evaluation results retain their existing order.

Records are read-only by API contract: core functions do not mutate caller inputs, including nested evidence, and callers treat assembly snapshots as immutable. `TypedDict` does not enforce runtime immutability; do not claim that it does. Defensive copies are required where an implementation would otherwise mutate input collections. Tests must exercise repeated calls and nested input preservation.

Keep the runtime dependency set empty unless implementation exposes a concrete need that is documented in the design. Build, static-checking, test, and JSON Schema validation tools are development dependencies. No SDK or data/agent framework becomes a core dependency.

### 2. Preserve the Sans I/O boundary

Domain entry points consume typed, materialized values and return typed, materialized values synchronously. Pure JSON encoding and decoding operate on supplied strings or values. Filesystem access, schema-resource loading, processes, environment configuration, network calls, databases, clocks, live agents, MCP sessions, and platform clients stay in adapters or development tooling.

Fixture values remain available without reading external files at domain-call time. The core root import must not eagerly import the fixture module or evaluate a demonstration episode. Normal Python module loading is not an application-level filesystem integration.

Platform packaging and MLflow integration may later wrap this library. They do not become prerequisites for installing, importing, validating, normalizing, or evaluating a case.

### 3. Version the interchange contract independently

Add checked-in JSON Schema Draft 2020-12 documents under a versioned schema directory. Define the shared domain records once and reference them from document schemas for logical assemblies, conformance cases, raw traces, trace-normalization results, validation results, and conformance evaluations. Include the schema artifacts in the Python distributions; loading them is a caller/tooling concern.

Version 1 documents use this envelope:

```json
{
  "schemaVersion": 1,
  "kind": "conformance-case",
  "value": {
    "assembly": {},
    "scenario": {}
  }
}
```

The example illustrates the envelope only; its abbreviated `value` is not a valid case. The allowed kind values are `logical-assembly`, `conformance-case`, `raw-trace`, `trace-normalization-result`, `validation-result`, and `conformance-evaluation`.

`schemaVersion` describes the interchange format. It is distinct from the package version and from `assembly.version`. Core domain functions continue to accept unwrapped typed payloads; the envelope belongs to pure interchange helpers and adapters. Those helpers report structured format findings for unsupported versions, mismatched kinds, invalid JSON, or incompatible payload shapes and do not pass rejected documents to the evaluator.

The wire contract retains existing field names, IDs, event and enum strings, validation paths, and result structures. Additional rules are explicit:

- Omitted optional fields remain omitted on a round trip. Do not fill them with `null`, empty strings, or empty collections. A JSON `null` inside a `JsonValue` field remains `null`; `null` is invalid for optional fields whose declared type does not include it.
- Preserve array order. JSON object-key order and textual whitespace are not semantic.
- Accept finite JSON numbers; reject NaN, infinities, and integer-valued numbers outside the JavaScript safe-integer range at the interchange boundary. Do not coerce strings to numbers or booleans to integers. These are wire restrictions, not new checks in the existing semantic validators.
- Reject unknown structural properties, while allowing arbitrary JSON-compatible keys within declared evidence/value maps. Changes to the structural vocabulary require a deliberate contract-version decision.
- Version 1 does not implicitly interpret an unwrapped payload as a versioned document. Legacy values remain usable as materialized function inputs and can be wrapped explicitly by an adapter.

Schema and decoder validation check shape rather than business validity. Structurally representable but semantically invalid values must still reach the existing domain validators: empty required strings or arrays, dangling IDs, unknown raw event-type strings, absent raw actors, and negative, fractional, or duplicate numeric sequence values. Raw trace types are intentionally more permissive than normalized event types. This preserves the current structured findings rather than replacing them with model-constructor exceptions.

### 4. Preserve behavior through a recorded reference corpus

Before changing or removing TypeScript code, record the reference source revision, any relevant working-tree diff, runtime/tool versions, and the commands used to produce a corpus of JSON inputs and expected outputs. Capture outputs from the actual TypeScript implementation, not a Python reimplementation of expected behavior.

The corpus covers every public behavioral function, the reference fixture, the existing test cases, and additional migration-sensitive edges. Type-only exports are covered by the API inventory, typing, and schema tests. Cover at least:

- The complete passing service-scheduling episode and all eight evaluation dimensions.
- Duplicate and dangling IDs; mismatched assembly, version, and state references; invalid projection references.
- Unknown events, empty or missing actors, negative/fractional/duplicate sequences, stable ordering for equal sequences, and omitted sequences.
- Stale and disputed provenance; omitted projections or operational facts; missing and late confirmation; prohibited transitions/outcomes; missing attribution.
- Empty collections and optional-field omission; nested evidence with `false`, `0`, empty strings, and `null`; repeatability and input non-mutation.

Keep semantic parity and format-validation tests separate. The reference corpus covers the current API's structurally typed, JSON-representable input domain within the new wire numeric bounds, including values intentionally rejected by semantic validation. Existing TypeScript behavior for inputs outside its declared types or outside this wire domain does not define a new Python compatibility promise.

Compare parsed payloads after normalizing only JSON object-key order and numeric spelling that denotes the same JSON number. Preserve JSON scalar types: booleans and numbers must not compare equal merely because Python considers `True == 1`. Array order, event positions, finding order, codes, severity, paths, messages, attribution, IDs, and evidence references must match. Do not suppress finding differences or reduce comparison to `valid`/`conformant` flags.

For set-returning helpers only, the corpus harness uses an explicit set encoding with sorted members and compares membership. Do not serialize a JavaScript `Set` directly as JSON, which would lose its members. This helper-specific encoding does not permit sorting any domain/result array or hiding changes in evaluator ordering.

Port the current trace-ordering algorithm, including its omitted-sequence sentinel and stable input-order tie breaking. Preserve `trace:<position>` references and findings addressed to original input indices. Keep trace validation and normalization distinct: normalization's existing decisions about admitting an event are not expanded into new semantic validation. Preserve evaluation's finding deduplication and current warning/pass/fail aggregation.

The complete baseline corpus must match before cutover. An unexplained mismatch blocks retirement of the TypeScript implementation. If the baseline reveals a defect, capture it for a separate behavior change; do not silently fix it or regenerate expected outputs from Python to make parity pass.

### 5. One implementation after cutover

TypeScript and Python coexist only during implementation and differential verification. Commit the reusable JSON corpus and provenance as permanent regression assets. After parity and packaging checks pass, remove the TypeScript implementation, Node-based core tests/build scripts, obsolete core package metadata and lockfile, and tracked obsolete build artifacts. Remove ignored generated files only after verifying their exact scope.

Retain the reference source through version-control history and the recorded revision. Keep corpus provenance and the parity result summary so future maintainers can reproduce the comparison without carrying a second production evaluator. Once retired, Node is not required for normal Python builds, tests, or execution.

The migration breaks npm import compatibility. Audit repository consumers and any known integration references before cutover; update in-scope consumers and document the migration boundary. Do not infer the absence of external consumers solely from the package's private flag. A real consumer needing an additional migration path must be accounted for before retirement.

Update the README, package examples, and `.reffy/reffyspec/project.md` when implementation lands. At archival, apply the requirement rename and modifications to the existing capability and update its purpose to describe Python. Preserve historical artifacts and archived proposals rather than rewriting them to imply Python was always the implementation.

### 6. Alternatives considered

- **Keep TypeScript and add Python adapters:** preserves native Node/browser evaluation, but Python consumers would need a process/service boundary or duplicate logic. Prefer this if browser/Node execution becomes a primary requirement before implementation starts.
- **Maintain both cores permanently:** offers direct imports in both ecosystems, but creates two places to evolve evaluation semantics and an ongoing parity obligation. The current project size does not justify that commitment.
- **Use a runtime model framework for the port:** may help a future ingestion layer, but default coercion and constructor errors could change current validation behavior. Typed records plus an explicit wire boundary make the compatibility obligations visible.

## Migration Sequence

1. Inventory exports and consumers; record the TypeScript baseline and JSON regression corpus.
2. Define and test version 1 schemas and interchange rules against that corpus.
3. Implement the Python package, fixtures, helpers, validators, normalizer, evaluator, and interchange functions.
4. Compare both implementations, run typing and schema checks, and verify wheel/source installation in clean environments.
5. Retire the TypeScript core, verify the retained Python regression path without Node, update active documentation, and archive the completed change.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Python equality, collection iteration, or omission handling changes results | Type-aware JSON comparison, ordering cases, and exact findings in the shared corpus |
| Structural validation swallows existing semantic findings | Separate wire-shape checks from domain checks and include intentionally invalid cases |
| Schemas and Python types drift | Validate accepted/rejected examples and serialized package outputs against checked-in schemas |
| Migration expands into evaluator redesign | Freeze the baseline and record semantic improvements separately |
| A Node consumer is overlooked | Audit known consumers before removing the npm surface |
| Porting delays proving the domain model | Keep the work limited to current behavior, interchange, and packaging; defer the workbench and integrations |

## Acceptance Evidence

- Export inventory mapping every current public symbol to its Python equivalent or explicitly documented type representation.
- Recorded TypeScript source provenance, regression inputs/outputs, and a differential comparison with no unexplained mismatches.
- Passing Python static checks, behavioral regression tests, JSON schema/round-trip tests, and input non-mutation tests.
- Wheel and source distribution installation tests outside the source tree, including fixture imports and one complete evaluation, with no Node or platform SDK required.
- Updated development documentation and a final Python-only check after TypeScript retirement.
- Successful Reffy change/manifest validation and an archive preview affecting only the intended capability.

## Open Questions

No product decision blocks this proposal. The implementation inventory must verify whether any known consumers require coordinated migration, and the development interpreter/tool versions must be recorded when the Python environment is established. Public registry naming and live platform deployment remain outside scope.
