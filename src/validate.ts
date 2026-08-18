import type { ConformanceCase } from "./conformance.js";
import { validationResult, type ValidationFinding, type ValidationResult } from "./domain.js";
import type { HarnessDescriptor } from "./harness.js";
import { logicalAssemblyEntries, logicalAssemblyEntryIds, type LasmProjectionReferences, type LogicalAssemblySlice } from "./lasm.js";
import { mcpPrimitives, type McpSurfaceDescriptor } from "./mcp.js";
import type { ActorObservation, OperationalState, OutcomeExpectation, StateTransitionExpectation } from "./operational-state.js";
import type { Scenario } from "./scenario.js";
import type { SkillDescriptor } from "./skill.js";
import { isAgenticEventType, type RawTraceEvent } from "./trace.js";

function required(value: string, path: string, findings: ValidationFinding[]): void {
  if (!value.trim()) {
    findings.push({ code: "fixture.required", severity: "error", path, message: "A non-empty value is required." });
  }
}

function nonEmpty(values: readonly unknown[], path: string, findings: ValidationFinding[]): void {
  if (values.length === 0) {
    findings.push({ code: "fixture.non_empty", severity: "error", path, message: "At least one item is required." });
  }
}

function uniqueIds(ids: readonly string[], path: string, findings: ValidationFinding[]): void {
  const duplicates = ids.filter((id, index) => ids.indexOf(id) !== index);
  for (const id of new Set(duplicates)) {
    findings.push({ code: "fixture.duplicate_id", severity: "error", path, message: `Duplicate id: ${id}` });
  }
}

function reference(
  id: string,
  knownIds: ReadonlySet<string>,
  path: string,
  code: string,
  label: string,
  findings: ValidationFinding[],
): void {
  if (!knownIds.has(id)) {
    findings.push({ code, severity: "error", path, message: `Unknown ${label}: ${id}` });
  }
}

function validateProjectionReferences(
  projection: LasmProjectionReferences | undefined,
  path: string,
  assemblyEntryIds: ReadonlySet<string> | undefined,
  stateFieldIds: ReadonlySet<string> | undefined,
  findings: ValidationFinding[],
): void {
  if (projection === undefined) return;
  const stateIds = projection.stateFieldIds ?? [];
  if (projection.assemblyEntryIds.length === 0 && stateIds.length === 0) {
    findings.push({
      code: "projection.empty",
      severity: "error",
      path,
      message: "A projection must reference assembly entries or operational-state fields.",
    });
  }
  uniqueIds(projection.assemblyEntryIds, `${path}.assemblyEntryIds`, findings);
  uniqueIds(stateIds, `${path}.stateFieldIds`, findings);
  if (assemblyEntryIds !== undefined) {
    projection.assemblyEntryIds.forEach((id, index) => reference(
      id,
      assemblyEntryIds,
      `${path}.assemblyEntryIds[${index}]`,
      "projection.unknown_assembly_entry",
      "assembly entry",
      findings,
    ));
  }
  if (stateFieldIds !== undefined) {
    stateIds.forEach((id, index) => reference(
      id,
      stateFieldIds,
      `${path}.stateFieldIds[${index}]`,
      "projection.unknown_state_field",
      "state field",
      findings,
    ));
  }
}

export function validateLogicalAssembly(assembly: LogicalAssemblySlice): ValidationResult {
  const findings: ValidationFinding[] = [];
  required(assembly.id, "assembly.id", findings);
  required(assembly.version, "assembly.version", findings);
  required(assembly.title, "assembly.title", findings);
  required(assembly.description, "assembly.description", findings);
  nonEmpty(assembly.provenance, "assembly.provenance", findings);
  nonEmpty(assembly.concepts, "assembly.concepts", findings);
  nonEmpty(assembly.evaluations, "assembly.evaluations", findings);

  uniqueIds(assembly.provenance.map(({ id }) => id), "assembly.provenance", findings);
  const sourceIds = new Set(assembly.provenance.map(({ id }) => id));
  assembly.provenance.forEach((source, index) => {
    required(source.id, `assembly.provenance[${index}].id`, findings);
    required(source.title, `assembly.provenance[${index}].title`, findings);
    required(source.locator, `assembly.provenance[${index}].locator`, findings);
  });

  const entries = logicalAssemblyEntries(assembly);
  uniqueIds(entries.map(({ id }) => id), "assembly.entries", findings);
  const entryIds = new Set(entries.map(({ id }) => id));
  const conceptIds = new Set(assembly.concepts.map(({ id }) => id));
  entries.forEach((entry, index) => {
    required(entry.id, `assembly.entries[${index}].id`, findings);
    required(entry.name, `assembly.entries[${index}].name`, findings);
    required(entry.description, `assembly.entries[${index}].description`, findings);
    nonEmpty(entry.sourceIds, `assembly.entries[${index}].sourceIds`, findings);
    entry.sourceIds.forEach((id, sourceIndex) => reference(
      id,
      sourceIds,
      `assembly.entries[${index}].sourceIds[${sourceIndex}]`,
      "assembly.unknown_provenance",
      "provenance source",
      findings,
    ));
  });

  assembly.relations.forEach((relation, index) => {
    reference(relation.fromConceptId, conceptIds, `assembly.relations[${index}].fromConceptId`, "assembly.unknown_concept", "concept", findings);
    reference(relation.toConceptId, conceptIds, `assembly.relations[${index}].toConceptId`, "assembly.unknown_concept", "concept", findings);
    required(relation.predicate, `assembly.relations[${index}].predicate`, findings);
  });
  assembly.constraints.forEach((constraint, index) => {
    nonEmpty(constraint.appliesToEntryIds, `assembly.constraints[${index}].appliesToEntryIds`, findings);
    constraint.appliesToEntryIds.forEach((id, refIndex) => reference(
      id,
      entryIds,
      `assembly.constraints[${index}].appliesToEntryIds[${refIndex}]`,
      "assembly.unknown_entry",
      "assembly entry",
      findings,
    ));
    required(constraint.rule, `assembly.constraints[${index}].rule`, findings);
  });
  assembly.events.forEach((event, index) => {
    nonEmpty(event.subjectConceptIds, `assembly.events[${index}].subjectConceptIds`, findings);
    event.subjectConceptIds.forEach((id, refIndex) => reference(
      id,
      conceptIds,
      `assembly.events[${index}].subjectConceptIds[${refIndex}]`,
      "assembly.unknown_concept",
      "concept",
      findings,
    ));
  });
  assembly.policies.forEach((policy, index) => {
    nonEmpty(policy.appliesToEntryIds, `assembly.policies[${index}].appliesToEntryIds`, findings);
    nonEmpty(policy.authorityRoles, `assembly.policies[${index}].authorityRoles`, findings);
    policy.appliesToEntryIds.forEach((id, refIndex) => reference(
      id,
      entryIds,
      `assembly.policies[${index}].appliesToEntryIds[${refIndex}]`,
      "assembly.unknown_entry",
      "assembly entry",
      findings,
    ));
    required(policy.commitment, `assembly.policies[${index}].commitment`, findings);
  });
  assembly.evaluations.forEach((evaluation, index) => {
    nonEmpty(evaluation.addressedEntryIds, `assembly.evaluations[${index}].addressedEntryIds`, findings);
    evaluation.addressedEntryIds.forEach((id, refIndex) => reference(
      id,
      entryIds,
      `assembly.evaluations[${index}].addressedEntryIds[${refIndex}]`,
      "assembly.unknown_entry",
      "assembly entry",
      findings,
    ));
    required(evaluation.evaluatorId, `assembly.evaluations[${index}].evaluatorId`, findings);
  });
  return validationResult(findings);
}

export function validateOperationalState(state: OperationalState, assembly: LogicalAssemblySlice): ValidationResult {
  const findings: ValidationFinding[] = [];
  required(state.id, "initialState.id", findings);
  if (state.assemblyId !== assembly.id) {
    findings.push({ code: "state.assembly_mismatch", severity: "error", path: "initialState.assemblyId", message: "Initial state references a different assembly." });
  }
  if (state.assemblyVersion !== assembly.version) {
    findings.push({ code: "state.version_mismatch", severity: "error", path: "initialState.assemblyVersion", message: "Initial state references a different assembly version." });
  }
  nonEmpty(state.fields, "initialState.fields", findings);
  uniqueIds(state.fields.map(({ id }) => id), "initialState.fields", findings);
  const conceptIds = new Set(assembly.concepts.map(({ id }) => id));
  state.fields.forEach((field, index) => {
    required(field.id, `initialState.fields[${index}].id`, findings);
    reference(field.conceptId, conceptIds, `initialState.fields[${index}].conceptId`, "state.unknown_concept", "concept", findings);
  });
  return validationResult(findings);
}

export function validateActorObservation(observation: ActorObservation, state: OperationalState): ValidationResult {
  const findings: ValidationFinding[] = [];
  required(observation.id, "observation.id", findings);
  required(observation.actorId, "observation.actorId", findings);
  nonEmpty(observation.fieldIds, "observation.fieldIds", findings);
  const fieldIds = new Set(state.fields.map(({ id }) => id));
  observation.fieldIds.forEach((id, index) => reference(
    id,
    fieldIds,
    `observation.fieldIds[${index}]`,
    "observation.unknown_state_field",
    "state field",
    findings,
  ));
  return validationResult(findings);
}

export function validateStateTransition(
  transition: StateTransitionExpectation,
  state: OperationalState,
  assembly: LogicalAssemblySlice,
): ValidationResult {
  const findings: ValidationFinding[] = [];
  required(transition.id, "transition.id", findings);
  required(transition.description, "transition.description", findings);
  nonEmpty(transition.fieldIds, "transition.fieldIds", findings);
  const fieldIds = new Set(state.fields.map(({ id }) => id));
  transition.fieldIds.forEach((id, index) => reference(
    id,
    fieldIds,
    `transition.fieldIds[${index}]`,
    "transition.unknown_state_field",
    "state field",
    findings,
  ));
  if (transition.eventId !== undefined) {
    reference(
      transition.eventId,
      new Set(assembly.events.map(({ id }) => id)),
      "transition.eventId",
      "transition.unknown_event",
      "assembly event",
      findings,
    );
  }
  return validationResult(findings);
}

export function validateOutcome(outcome: OutcomeExpectation, state: OperationalState): ValidationResult {
  const findings: ValidationFinding[] = [];
  required(outcome.id, "outcome.id", findings);
  required(outcome.description, "outcome.description", findings);
  nonEmpty(outcome.fieldIds, "outcome.fieldIds", findings);
  const fieldIds = new Set(state.fields.map(({ id }) => id));
  outcome.fieldIds.forEach((id, index) => reference(
    id,
    fieldIds,
    `outcome.fieldIds[${index}]`,
    "outcome.unknown_state_field",
    "state field",
    findings,
  ));
  return validationResult(findings);
}

export function validateScenario(scenario: Scenario): ValidationResult {
  const findings: ValidationFinding[] = [];
  required(scenario.id, "scenario.id", findings);
  required(scenario.title, "scenario.title", findings);
  required(scenario.businessContext.summary, "scenario.businessContext.summary", findings);
  required(scenario.intent.explicitGoal, "scenario.intent.explicitGoal", findings);
  required(scenario.reality.assemblyId, "scenario.reality.assemblyId", findings);
  required(scenario.reality.assemblyVersion, "scenario.reality.assemblyVersion", findings);
  required(scenario.reality.initialStateId, "scenario.reality.initialStateId", findings);
  nonEmpty(scenario.businessContext.stakeholders, "scenario.businessContext.stakeholders", findings);
  nonEmpty(scenario.businessContext.requiredFacts, "scenario.businessContext.requiredFacts", findings);
  nonEmpty(scenario.reality.assemblyEntryIds, "scenario.reality.assemblyEntryIds", findings);
  nonEmpty(scenario.reality.observationIds, "scenario.reality.observationIds", findings);
  nonEmpty(scenario.reality.transitionIds, "scenario.reality.transitionIds", findings);
  nonEmpty(scenario.reality.outcomeIds, "scenario.reality.outcomeIds", findings);
  nonEmpty(scenario.expectedControlSurfaces.harnessIds, "scenario.expectedControlSurfaces.harnessIds", findings);
  uniqueIds(
    [
      ...scenario.expectedControlSurfaces.harnessIds,
      ...scenario.expectedControlSurfaces.skillIds,
      ...scenario.expectedControlSurfaces.mcpServerIds,
      ...scenario.expectedControlSurfaces.mcpPrimitiveIds,
    ],
    "scenario.expectedControlSurfaces",
    findings,
  );
  return validationResult(findings);
}

export function validateHarness(
  harness: HarnessDescriptor,
  assembly?: LogicalAssemblySlice,
  state?: OperationalState,
): ValidationResult {
  const findings: ValidationFinding[] = [];
  required(harness.id, "harness.id", findings);
  required(harness.name, "harness.name", findings);
  required(harness.purpose, "harness.purpose", findings);
  nonEmpty(harness.contextSurfaces, "harness.contextSurfaces", findings);
  nonEmpty(harness.affordances, "harness.affordances", findings);
  nonEmpty(harness.permissionModel.scopedPermissions, "harness.permissionModel.scopedPermissions", findings);
  nonEmpty(harness.handoffBoundaries, "harness.handoffBoundaries", findings);
  uniqueIds(harness.contextSurfaces.map(({ id }) => id), "harness.contextSurfaces", findings);
  uniqueIds(harness.handoffBoundaries.map(({ id }) => id), "harness.handoffBoundaries", findings);
  const entryIds = assembly === undefined ? undefined : logicalAssemblyEntryIds(assembly);
  const fieldIds = state === undefined ? undefined : new Set(state.fields.map(({ id }) => id));
  validateProjectionReferences(harness.projection, "harness.projection", entryIds, fieldIds, findings);
  harness.contextSurfaces.forEach((surface, index) => validateProjectionReferences(surface.projection, `harness.contextSurfaces[${index}].projection`, entryIds, fieldIds, findings));
  validateProjectionReferences(harness.permissionModel.projection, "harness.permissionModel.projection", entryIds, fieldIds, findings);
  validateProjectionReferences(harness.approvalFlow.projection, "harness.approvalFlow.projection", entryIds, fieldIds, findings);
  harness.handoffBoundaries.forEach((boundary, index) => validateProjectionReferences(boundary.projection, `harness.handoffBoundaries[${index}].projection`, entryIds, fieldIds, findings));
  return validationResult(findings);
}

export function validateSkill(
  skill: SkillDescriptor,
  assembly?: LogicalAssemblySlice,
  state?: OperationalState,
): ValidationResult {
  const findings: ValidationFinding[] = [];
  required(skill.id, "skill.id", findings);
  required(skill.name, "skill.name", findings);
  required(skill.purpose, "skill.purpose", findings);
  nonEmpty(skill.applicability, "skill.applicability", findings);
  nonEmpty(skill.capabilities, "skill.capabilities", findings);
  validateProjectionReferences(
    skill.projection,
    "skill.projection",
    assembly === undefined ? undefined : logicalAssemblyEntryIds(assembly),
    state === undefined ? undefined : new Set(state.fields.map(({ id }) => id)),
    findings,
  );
  return validationResult(findings);
}

export function validateMcpSurface(
  surface: McpSurfaceDescriptor,
  assembly?: LogicalAssemblySlice,
  state?: OperationalState,
): ValidationResult {
  const findings: ValidationFinding[] = [];
  required(surface.id, "mcp.id", findings);
  required(surface.name, "mcp.name", findings);
  required(surface.purpose, "mcp.purpose", findings);
  const primitives = mcpPrimitives(surface);
  nonEmpty(primitives, "mcp.primitives", findings);
  uniqueIds(primitives.map(({ id }) => id), "mcp.primitives", findings);
  const entryIds = assembly === undefined ? undefined : logicalAssemblyEntryIds(assembly);
  const fieldIds = state === undefined ? undefined : new Set(state.fields.map(({ id }) => id));
  validateProjectionReferences(surface.projection, "mcp.projection", entryIds, fieldIds, findings);
  for (const [index, primitive] of primitives.entries()) {
    required(primitive.id, `mcp.primitives[${index}].id`, findings);
    required(primitive.name, `mcp.primitives[${index}].name`, findings);
    required(primitive.purpose, `mcp.primitives[${index}].purpose`, findings);
    validateProjectionReferences(primitive.projection, `mcp.primitives[${index}].projection`, entryIds, fieldIds, findings);
  }
  return validationResult(findings);
}

export function validateTrace(trace: readonly RawTraceEvent[]): ValidationResult {
  const findings: ValidationFinding[] = [];
  nonEmpty(trace, "trace", findings);
  const sequences = trace.flatMap((event) => event.sequence === undefined ? [] : [event.sequence]);
  uniqueIds(sequences.map(String), "trace.sequence", findings);

  trace.forEach((event, index) => {
    if (!isAgenticEventType(event.type)) {
      findings.push({
        code: "trace.unknown_event_type",
        severity: "error",
        path: `trace[${index}].type`,
        message: `Unknown agentic event type: ${event.type || "<empty>"}`,
      });
    }
    if (!event.actorId?.trim()) {
      findings.push({
        code: "trace.missing_actor",
        severity: "error",
        path: `trace[${index}].actorId`,
        message: "Trace events require an actor identifier.",
      });
    }
    if (event.sequence !== undefined && (!Number.isInteger(event.sequence) || event.sequence < 0)) {
      findings.push({
        code: "trace.invalid_sequence",
        severity: "error",
        path: `trace[${index}].sequence`,
        message: "Sequence must be a non-negative integer.",
      });
    }
  });
  return validationResult(findings);
}

export function validateConformanceCase(input: ConformanceCase): ValidationResult {
  const findings: ValidationFinding[] = [
    ...validateLogicalAssembly(input.assembly).findings,
    ...validateOperationalState(input.initialState, input.assembly).findings,
    ...validateScenario(input.scenario).findings,
    ...input.observations.flatMap((observation) => validateActorObservation(observation, input.initialState).findings),
    ...input.transitions.flatMap((transition) => validateStateTransition(transition, input.initialState, input.assembly).findings),
    ...input.outcomes.flatMap((outcome) => validateOutcome(outcome, input.initialState).findings),
    ...input.harnesses.flatMap((harness) => validateHarness(harness, input.assembly, input.initialState).findings),
    ...input.skills.flatMap((skill) => validateSkill(skill, input.assembly, input.initialState).findings),
    ...input.mcpSurfaces.flatMap((surface) => validateMcpSurface(surface, input.assembly, input.initialState).findings),
    ...validateTrace(input.trace).findings,
  ];

  const reality = input.scenario.reality;
  const assemblyEntryIds = logicalAssemblyEntryIds(input.assembly);
  const observationIds = new Set(input.observations.map(({ id }) => id));
  const transitionIds = new Set(input.transitions.map(({ id }) => id));
  const outcomeIds = new Set(input.outcomes.map(({ id }) => id));
  if (reality.assemblyId !== input.assembly.id) {
    findings.push({ code: "scenario.assembly_mismatch", severity: "error", path: "scenario.reality.assemblyId", message: "Scenario references a different assembly." });
  }
  if (reality.assemblyVersion !== input.assembly.version) {
    findings.push({ code: "scenario.version_mismatch", severity: "error", path: "scenario.reality.assemblyVersion", message: "Scenario references a different assembly version." });
  }
  if (reality.initialStateId !== input.initialState.id) {
    findings.push({ code: "scenario.state_mismatch", severity: "error", path: "scenario.reality.initialStateId", message: "Scenario references a different initial state." });
  }
  reality.assemblyEntryIds.forEach((id, index) => reference(id, assemblyEntryIds, `scenario.reality.assemblyEntryIds[${index}]`, "scenario.unknown_assembly_entry", "assembly entry", findings));
  reality.observationIds.forEach((id, index) => reference(id, observationIds, `scenario.reality.observationIds[${index}]`, "scenario.unknown_observation", "observation", findings));
  reality.transitionIds.forEach((id, index) => reference(id, transitionIds, `scenario.reality.transitionIds[${index}]`, "scenario.unknown_transition", "transition", findings));
  reality.outcomeIds.forEach((id, index) => reference(id, outcomeIds, `scenario.reality.outcomeIds[${index}]`, "scenario.unknown_outcome", "outcome", findings));

  const expected = input.scenario.expectedControlSurfaces;
  const fixtureIds = {
    harness: new Set(input.harnesses.map(({ id }) => id)),
    skill: new Set(input.skills.map(({ id }) => id)),
    server: new Set(input.mcpSurfaces.map(({ id }) => id)),
    primitive: new Set(input.mcpSurfaces.flatMap(mcpPrimitives).map(({ id }) => id)),
  };
  expected.harnessIds.forEach((id, index) => reference(id, fixtureIds.harness, `scenario.expectedControlSurfaces.harnessIds[${index}]`, "scenario.unknown_harness", "harness", findings));
  expected.skillIds.forEach((id, index) => reference(id, fixtureIds.skill, `scenario.expectedControlSurfaces.skillIds[${index}]`, "scenario.unknown_skill", "skill", findings));
  expected.mcpServerIds.forEach((id, index) => reference(id, fixtureIds.server, `scenario.expectedControlSurfaces.mcpServerIds[${index}]`, "scenario.unknown_mcp_server", "MCP server", findings));
  expected.mcpPrimitiveIds.forEach((id, index) => reference(id, fixtureIds.primitive, `scenario.expectedControlSurfaces.mcpPrimitiveIds[${index}]`, "scenario.unknown_mcp_primitive", "MCP primitive", findings));

  uniqueIds(input.observations.map(({ id }) => id), "observations", findings);
  uniqueIds(input.transitions.map(({ id }) => id), "transitions", findings);
  uniqueIds(input.outcomes.map(({ id }) => id), "outcomes", findings);
  uniqueIds(input.harnesses.map(({ id }) => id), "harnesses", findings);
  uniqueIds(input.skills.map(({ id }) => id), "skills", findings);
  uniqueIds(input.mcpSurfaces.map(({ id }) => id), "mcpSurfaces", findings);

  return validationResult(findings);
}
