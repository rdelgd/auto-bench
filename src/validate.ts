import { validationResult, type ValidationFinding, type ValidationResult } from "./domain.js";
import type { HarnessDescriptor } from "./harness.js";
import { mcpPrimitives, type McpSurfaceDescriptor } from "./mcp.js";
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

export function validateScenario(scenario: Scenario): ValidationResult {
  const findings: ValidationFinding[] = [];
  required(scenario.id, "scenario.id", findings);
  required(scenario.title, "scenario.title", findings);
  required(scenario.businessContext.summary, "scenario.businessContext.summary", findings);
  required(scenario.intent.explicitGoal, "scenario.intent.explicitGoal", findings);
  nonEmpty(scenario.businessContext.stakeholders, "scenario.businessContext.stakeholders", findings);
  nonEmpty(scenario.businessContext.requiredFacts, "scenario.businessContext.requiredFacts", findings);
  nonEmpty(scenario.expectedOutcomes, "scenario.expectedOutcomes", findings);
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

export function validateHarness(harness: HarnessDescriptor): ValidationResult {
  const findings: ValidationFinding[] = [];
  required(harness.id, "harness.id", findings);
  required(harness.name, "harness.name", findings);
  required(harness.purpose, "harness.purpose", findings);
  nonEmpty(harness.contextSurfaces, "harness.contextSurfaces", findings);
  nonEmpty(harness.affordances, "harness.affordances", findings);
  nonEmpty(harness.permissionModel.scopedPermissions, "harness.permissionModel.scopedPermissions", findings);
  nonEmpty(harness.handoffBoundaries, "harness.handoffBoundaries", findings);
  uniqueIds(harness.contextSurfaces.map(({ id }) => id), "harness.contextSurfaces", findings);
  return validationResult(findings);
}

export function validateSkill(skill: SkillDescriptor): ValidationResult {
  const findings: ValidationFinding[] = [];
  required(skill.id, "skill.id", findings);
  required(skill.name, "skill.name", findings);
  required(skill.purpose, "skill.purpose", findings);
  nonEmpty(skill.applicability, "skill.applicability", findings);
  nonEmpty(skill.capabilities, "skill.capabilities", findings);
  return validationResult(findings);
}

export function validateMcpSurface(surface: McpSurfaceDescriptor): ValidationResult {
  const findings: ValidationFinding[] = [];
  required(surface.id, "mcp.id", findings);
  required(surface.name, "mcp.name", findings);
  required(surface.purpose, "mcp.purpose", findings);
  const primitives = mcpPrimitives(surface);
  nonEmpty(primitives, "mcp.primitives", findings);
  uniqueIds(primitives.map(({ id }) => id), "mcp.primitives", findings);
  for (const [index, primitive] of primitives.entries()) {
    required(primitive.id, `mcp.primitives[${index}].id`, findings);
    required(primitive.name, `mcp.primitives[${index}].name`, findings);
    required(primitive.purpose, `mcp.primitives[${index}].purpose`, findings);
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
