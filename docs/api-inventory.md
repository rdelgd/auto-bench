# `@lasm/core` → `lasm_core` API Inventory

This inventory maps every public export of the retired TypeScript package `@lasm/core@0.1.0`
(source revision `56460752edfe8a17e4f761d141ec2bb7a0f704f4`) to its Python equivalent in `lasm-core`.
It is checked by `tests/test_package_identity.py`, which fails if a public Python symbol is missing here.

Conventions:

- Functions and modules use snake_case; domain type names are unchanged.
- Records are `TypedDict`s whose keys are the existing camelCase wire names, so payloads are unchanged.
- TypeScript optional properties (`?:`) are `NotRequired` keys: they are omitted, never `None`.
- TypeScript `readonly T[]` is `Sequence[T]`; `Readonly<Record<string, JsonValue>>` is `Mapping[str, JsonValue]`.
  Records are read-only by API contract; `TypedDict` does not enforce immutability at runtime.
- Optional TypeScript parameters (`assembly?`, `state?`) default to `None`.

## Root: `@lasm/core` → `lasm_core`

### Functions and constants

| TypeScript | Python | Notes |
| --- | --- | --- |
| `validationResult` | `validation_result` | |
| `logicalAssemblyEntries` | `logical_assembly_entries` | Returns a new `list`. |
| `logicalAssemblyEntryIds` | `logical_assembly_entry_ids` | Returns `frozenset[str]` (was `ReadonlySet<string>`). Compatibility promise is membership. |
| `mcpPrimitives` | `mcp_primitives` | Returns a new `list`: tools, resources, prompts. |
| `agenticEventTypes` | `AGENTIC_EVENT_TYPES` | Ordered `tuple`, derived from the `AgenticEventType` literal. |
| `isAgenticEventType` | `is_agentic_event_type` | `TypeGuard[AgenticEventType]`. |
| `traceEvidenceRef` | `trace_evidence_ref` | |
| `normalizeTrace` | `normalize_trace` | |
| `validateLogicalAssembly` | `validate_logical_assembly` | |
| `validateOperationalState` | `validate_operational_state` | |
| `validateActorObservation` | `validate_actor_observation` | |
| `validateStateTransition` | `validate_state_transition` | |
| `validateOutcome` | `validate_outcome` | |
| `validateScenario` | `validate_scenario` | |
| `validateHarness` | `validate_harness` | |
| `validateSkill` | `validate_skill` | |
| `validateMcpSurface` | `validate_mcp_surface` | |
| `validateTrace` | `validate_trace` | Duplicate sequences compare numerically (`1` and `1.0` collide); messages use Python spelling (`1e-07`). |
| `validateConformanceCase` | `validate_conformance_case` | |
| `evaluateConformance` | `evaluate_conformance` | |

### Types

| TypeScript | Python | Representation |
| --- | --- | --- |
| `JsonPrimitive` | `JsonPrimitive` | `str \| int \| float \| bool \| None` |
| `JsonValue` | `JsonValue` | Recursive alias over `Sequence` and `Mapping[str, ...]` |
| `EvidencePayload` | `EvidencePayload` | `Mapping[str, JsonValue]` |
| `ValidationSeverity` | `ValidationSeverity` | `Literal` |
| `ValidationFinding` | `ValidationFinding` | `TypedDict` |
| `ValidationResult` | `ValidationResult` | `TypedDict` |
| `ProvenanceKind` | `ProvenanceKind` | `Literal` |
| `ProvenanceStatus` | `ProvenanceStatus` | `Literal` |
| `ProvenanceSource` | `ProvenanceSource` | `TypedDict` |
| `LasmEntryBase` | `LasmEntryBase` | `TypedDict` base |
| `ConceptEntry` | `ConceptEntry` | `TypedDict` |
| `RelationEntry` | `RelationEntry` | `TypedDict` |
| `ConstraintEntry` | `ConstraintEntry` | `TypedDict` |
| `EventEntry` | `EventEntry` | `TypedDict` |
| `PolicyEntry` | `PolicyEntry` | `TypedDict` |
| `RuntimeEvaluationMode` | `RuntimeEvaluationMode` | `Literal` |
| `RuntimeEvaluationDescriptor` | `RuntimeEvaluationDescriptor` | `TypedDict` |
| `LogicalAssemblyEntry` | `LogicalAssemblyEntry` | `Union` of entry records |
| `LogicalAssemblySlice` | `LogicalAssemblySlice` | `TypedDict` |
| `LasmProjectionReferences` | `LasmProjectionReferences` | `TypedDict` |
| `InteractionMode` | `InteractionMode` | `Literal` |
| `PermissionLevel` | `PermissionLevel` | `Literal` |
| `ContextSurface` | `ContextSurface` | `TypedDict` |
| `ContextSurface["sensitivity"]` (inline union) | `ContextSensitivity` | Newly named `Literal` |
| `HandoffBoundary` | `HandoffBoundary` | `TypedDict` |
| `HarnessDescriptor["permissionModel"]` (inline) | `PermissionModel` | Newly named `TypedDict` |
| `HarnessDescriptor["approvalFlow"]` (inline) | `ApprovalFlow` | Newly named `TypedDict` |
| `HarnessDescriptor` | `HarnessDescriptor` | `TypedDict` |
| `SkillReference` | `SkillReference` | `TypedDict` |
| `SkillReference["kind"]` (inline union) | `SkillReferenceKind` | Newly named `Literal` |
| `SkillDescriptor` | `SkillDescriptor` | `TypedDict` |
| `McpRisk` | `McpRisk` | `Literal` |
| `McpPrimitiveDescriptor` | `McpPrimitiveDescriptor` | `TypedDict` |
| `McpSurfaceDescriptor` | `McpSurfaceDescriptor` | `TypedDict` |
| `OperationalStateField` | `OperationalStateField` | `TypedDict` |
| `OperationalState` | `OperationalState` | `TypedDict` |
| `ActorObservation` | `ActorObservation` | `TypedDict` |
| `TransitionDisposition` | `TransitionDisposition` | `Literal` |
| `StateTransitionExpectation` | `StateTransitionExpectation` | `TypedDict` |
| `OutcomeDisposition` | `OutcomeDisposition` | `Literal` |
| `OutcomeExpectation` | `OutcomeExpectation` | `TypedDict` |
| `AutomotiveDomain` | `AutomotiveDomain` | `Literal` |
| `BusinessContext` | `BusinessContext` | `TypedDict` |
| `UserIntent` | `UserIntent` | `TypedDict` |
| `ExpectedControlSurfaces` | `ExpectedControlSurfaces` | `TypedDict` |
| `RealityReferenceSet` | `RealityReferenceSet` | `TypedDict` |
| `EvaluationExpectations` | `EvaluationExpectations` | `TypedDict` |
| `Scenario` | `Scenario` | `TypedDict` |
| `ConformanceCase` | `ConformanceCase` | `TypedDict` |
| `AgenticEventType` | `AgenticEventType` | `Literal` |
| `RawTraceEvent` | `RawTraceEvent` | `TypedDict`; `sequence` is `int \| float` |
| `NormalizedTraceEvent` | `NormalizedTraceEvent` | `TypedDict` |
| `TraceNormalizationResult` | `TraceNormalizationResult` | `TypedDict` |
| `EvaluationDimension` | `EvaluationDimension` | `Literal` |
| `EvaluationStatus` | `EvaluationStatus` | `Literal` |
| `EvaluationFindingSeverity` | `EvaluationFindingSeverity` | `Literal` |
| `DivergenceSource` | `DivergenceSource` | `Literal` |
| `EvaluationFinding` | `EvaluationFinding` | `TypedDict` |
| `DimensionResult` | `DimensionResult` | `TypedDict` |
| `ConformanceEvaluation` | `ConformanceEvaluation` | `TypedDict` |

### New in Python: versioned interchange

These have no TypeScript counterpart. They are pure: they operate on supplied strings and values.

| Python | Purpose |
| --- | --- |
| `DocumentKind`, `DOCUMENT_KINDS` | The six version 1 document kinds. |
| `SUPPORTED_SCHEMA_VERSIONS` | Interchange format versions accepted by the decoder (`(1,)`). |
| `wrap_document` | Wrap a payload in a `{schemaVersion, kind, value}` envelope. |
| `validate_document` | Check a parsed document; return its payload or structured `format.*` findings. |
| `decode_document` | Parse supplied JSON text, then `validate_document`. |
| `encode_document` | Validate and serialize a payload as a version 1 document. |
| `DocumentDecodeResult`, `DocumentEncodeResult` | Result records; `value`/`text` are absent when rejected. |

The checked-in JSON Schemas are packaged under `lasm_core/schemas/v1/`. Loading them is a caller concern.

## Fixtures: `@lasm/core/fixtures` → `lasm_core.fixtures`

| TypeScript | Python |
| --- | --- |
| `serviceSchedulingAssembly` | `service_scheduling_assembly` |
| `serviceSchedulingInitialState` | `service_scheduling_initial_state` |
| `serviceSchedulingObservations` | `service_scheduling_observations` |
| `serviceSchedulingTransitions` | `service_scheduling_transitions` |
| `serviceSchedulingOutcomes` | `service_scheduling_outcomes` |
| `serviceAdvisorHarness` | `service_advisor_harness` |
| `serviceSchedulingSkill` | `service_scheduling_skill` |
| `dealershipOperationsMcp` | `dealership_operations_mcp` |
| `routineMaintenanceScenario` | `routine_maintenance_scenario` |
| `routineMaintenanceTrace` | `routine_maintenance_trace` |
| `routineMaintenanceConformanceCase` | `routine_maintenance_conformance_case` |
| `routineMaintenanceEvaluation` | `routine_maintenance_evaluation` |

`lasm_core` does not import `lasm_core.fixtures`. As in TypeScript, `routine_maintenance_evaluation`
is computed when the fixtures module is first imported.

## Added After Migration

These exports have no TypeScript counterpart. They were added by the `add-weight-patch-projection-surface`
change and are covered by ordinary tests rather than the TypeScript reference corpus.

| Python | Representation | Purpose |
| --- | --- | --- |
| `WeightPatchDescriptor` | `TypedDict` | A compiled knowledge patch modeled as a Lasm projection: `id`, `name`, `purpose`, `baseModelId`, `digest`, required `projection`. |
| `validate_weight_patch` | function | Validates a descriptor's required fields and projection references against an optional assembly and state. |
| `ConformanceCase["weightPatches"]` | `NotRequired` | Omitted means no weight patches. |
| `ExpectedControlSurfaces["weightPatchIds"]` | `NotRequired` | Omitted means none are expected. |
| `AgenticEventType` values `patch.applied`, `patch.probed` | `Literal` | Subject is the weight patch id; the evaluator reads `digest`, `probe`, and `passed` from evidence. |

Sales-domain reference fixture in `lasm_core.fixtures`:

| Python | Purpose |
| --- | --- |
| `new_vehicle_units_assembly` | Net new-vehicle units and the stock-type distinction. |
| `new_vehicle_units_initial_state` | Governed definition, stock-type scope, and the unreported figure. |
| `new_vehicle_units_observations` | The agent's observation of the governed definition. |
| `new_vehicle_units_transitions` | The permitted, required units-reported transition. |
| `new_vehicle_units_outcomes` | Acceptable all-stock-types outcome and prohibited retail-only outcome. |
| `sales_analyst_harness` | Read-only analytical harness. |
| `new_vehicle_units_skill` | Skill projecting the units definition. |
| `new_vehicle_units_weight_patch` | Weight patch claiming the units and stock-type concepts. |
| `new_vehicle_units_scenario` | The regional manager's question, expecting the harness, skill, and patch. |
| `new_vehicle_units_trace` | Patch applied with its digest, canonical probe passed, paraphrase probe failed, retail-only figure reported. |
| `new_vehicle_units_conformance_case` | The complete case. |
| `new_vehicle_units_evaluation` | Nonconformant: probe failure and divergence attributed to the patch, prohibited outcome observed. |

## Consumer Audit

Recorded on 2026-09-22 before retiring the npm package:

- In this repository, `@lasm/core` was referenced only by `package.json`, `package-lock.json`, `README.md`,
  `test/package-identity.test.ts`, the canonical spec, project context, Reffy artifacts, and archived changes.
  No source outside the package imported it.
- Sibling repositories under the same workspace (`dapps-poc`, `dvaa-azure-databricks`, `gaaar`, `gtm-containers`,
  `sammy-dev`, `data`) contain no `package.json` or source reference to `@lasm/core`.
- The package was `private: true` and never published. No known external consumer requires a coordinated migration.
