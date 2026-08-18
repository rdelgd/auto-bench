export type ProvenanceKind = "schema" | "code" | "policy" | "practice" | "incident" | "commitment" | "judgment";
export type ProvenanceStatus = "current" | "stale" | "disputed";

export interface ProvenanceSource {
  readonly id: string;
  readonly kind: ProvenanceKind;
  readonly title: string;
  readonly locator: string;
  readonly owner?: string;
  readonly version?: string;
  readonly observedAt?: string;
  readonly status: ProvenanceStatus;
}

export interface LasmEntryBase {
  readonly id: string;
  readonly name: string;
  readonly description: string;
  readonly sourceIds: readonly string[];
}

export interface ConceptEntry extends LasmEntryBase {
  readonly kind: "concept";
}

export interface RelationEntry extends LasmEntryBase {
  readonly kind: "relation";
  readonly fromConceptId: string;
  readonly toConceptId: string;
  readonly predicate: string;
}

export interface ConstraintEntry extends LasmEntryBase {
  readonly kind: "constraint";
  readonly appliesToEntryIds: readonly string[];
  readonly rule: string;
}

export interface EventEntry extends LasmEntryBase {
  readonly kind: "event";
  readonly subjectConceptIds: readonly string[];
}

export interface PolicyEntry extends LasmEntryBase {
  readonly kind: "policy";
  readonly appliesToEntryIds: readonly string[];
  readonly authorityRoles: readonly string[];
  readonly commitment: string;
}

export type RuntimeEvaluationMode = "gate" | "check";

export interface RuntimeEvaluationDescriptor extends LasmEntryBase {
  readonly kind: "evaluation";
  readonly mode: RuntimeEvaluationMode;
  readonly addressedEntryIds: readonly string[];
  readonly evaluatorId: string;
}

export type LogicalAssemblyEntry =
  | ConceptEntry
  | RelationEntry
  | ConstraintEntry
  | EventEntry
  | PolicyEntry
  | RuntimeEvaluationDescriptor;

export interface LogicalAssemblySlice {
  readonly id: string;
  readonly version: string;
  readonly title: string;
  readonly description: string;
  readonly provenance: readonly ProvenanceSource[];
  readonly concepts: readonly ConceptEntry[];
  readonly relations: readonly RelationEntry[];
  readonly constraints: readonly ConstraintEntry[];
  readonly events: readonly EventEntry[];
  readonly policies: readonly PolicyEntry[];
  readonly evaluations: readonly RuntimeEvaluationDescriptor[];
}

export interface LasmProjectionReferences {
  readonly assemblyEntryIds: readonly string[];
  readonly stateFieldIds?: readonly string[];
}

export function logicalAssemblyEntries(assembly: LogicalAssemblySlice): readonly LogicalAssemblyEntry[] {
  return [
    ...assembly.concepts,
    ...assembly.relations,
    ...assembly.constraints,
    ...assembly.events,
    ...assembly.policies,
    ...assembly.evaluations,
  ];
}

export function logicalAssemblyEntryIds(assembly: LogicalAssemblySlice): ReadonlySet<string> {
  return new Set(logicalAssemblyEntries(assembly).map(({ id }) => id));
}
