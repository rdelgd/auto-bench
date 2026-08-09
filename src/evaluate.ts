import type { ValidationFinding } from "./domain.js";
import type { HarnessDescriptor } from "./harness.js";
import { mcpPrimitives, type McpSurfaceDescriptor } from "./mcp.js";
import type { Scenario } from "./scenario.js";
import type { SkillDescriptor } from "./skill.js";
import { normalizeTrace, traceEvidenceRef, type AgenticEventType, type NormalizedTraceEvent, type RawTraceEvent } from "./trace.js";
import { validateHarness, validateMcpSurface, validateScenario, validateSkill, validateTrace } from "./validate.js";

export type EvaluationDimension =
  | "intent-fidelity"
  | "control-surface-quality"
  | "business-realism"
  | "observability"
  | "governance";
export type EvaluationStatus = "pass" | "warning" | "fail";
export type EvaluationFindingSeverity = "info" | "warning" | "error";

export interface EvaluationFinding {
  readonly code: string;
  readonly severity: EvaluationFindingSeverity;
  readonly message: string;
  readonly evidenceRefs: readonly string[];
}

export interface DimensionResult {
  readonly dimension: EvaluationDimension;
  readonly status: EvaluationStatus;
  readonly findings: readonly EvaluationFinding[];
  readonly evidenceRefs: readonly string[];
}

export interface BenchmarkInput {
  readonly scenario: Scenario;
  readonly harnesses: readonly HarnessDescriptor[];
  readonly skills: readonly SkillDescriptor[];
  readonly mcpSurfaces: readonly McpSurfaceDescriptor[];
  readonly trace: readonly RawTraceEvent[];
}

export interface BenchmarkEvaluation {
  readonly scenarioId: string;
  readonly valid: boolean;
  readonly validationFindings: readonly ValidationFinding[];
  readonly dimensions: readonly DimensionResult[];
}

function eventsOfType(events: readonly NormalizedTraceEvent[], ...types: AgenticEventType[]): readonly NormalizedTraceEvent[] {
  return events.filter(({ type }) => types.includes(type));
}

function subjectIds(events: readonly NormalizedTraceEvent[]): ReadonlySet<string> {
  return new Set(events.flatMap(({ subjectId }) => subjectId === undefined ? [] : [subjectId]));
}

function evidenceRefs(findings: readonly EvaluationFinding[]): readonly string[] {
  return [...new Set(findings.flatMap((finding) => finding.evidenceRefs))];
}

function result(dimension: EvaluationDimension, findings: readonly EvaluationFinding[]): DimensionResult {
  const status: EvaluationStatus = findings.some(({ severity }) => severity === "error")
    ? "fail"
    : findings.some(({ severity }) => severity === "warning")
      ? "warning"
      : "pass";
  return { dimension, status, findings, evidenceRefs: evidenceRefs(findings) };
}

function missingFinding(code: string, message: string, evidence: readonly string[] = []): EvaluationFinding {
  return { code, severity: "error", message, evidenceRefs: evidence };
}

function passingFinding(code: string, message: string, events: readonly NormalizedTraceEvent[]): EvaluationFinding {
  return { code, severity: "info", message, evidenceRefs: events.map(traceEvidenceRef) };
}

function evaluateIntent(scenario: Scenario, events: readonly NormalizedTraceEvent[]): DimensionResult {
  const submitted = eventsOfType(events, "intent.submitted");
  const outcomes = eventsOfType(events, "task.completed", "task.failed");
  const preserved = submitted.filter(({ evidence }) => evidence.goal === scenario.intent.explicitGoal);
  const findings: EvaluationFinding[] = [];
  findings.push(preserved.length > 0
    ? passingFinding("intent.explicit_goal_observed", "The submitted intent matches the scenario's explicit goal.", preserved)
    : missingFinding("intent.explicit_goal_missing", "The trace does not preserve the scenario's explicit goal.", submitted.map(traceEvidenceRef)));
  findings.push(outcomes.some(({ type }) => type === "task.completed")
    ? passingFinding("intent.outcome_completed", "The trace records a completed business outcome.", outcomes)
    : missingFinding("intent.outcome_incomplete", "The trace does not record successful task completion.", outcomes.map(traceEvidenceRef)));
  return result("intent-fidelity", findings);
}

function evaluateControlSurfaces(input: BenchmarkInput, events: readonly NormalizedTraceEvent[]): DimensionResult {
  const expected = input.scenario.expectedControlSurfaces;
  const fixtureHarnessIds = new Set(input.harnesses.map(({ id }) => id));
  const fixtureSkillIds = new Set(input.skills.map(({ id }) => id));
  const fixtureServerIds = new Set(input.mcpSurfaces.map(({ id }) => id));
  const fixturePrimitiveIds = new Set(input.mcpSurfaces.flatMap(mcpPrimitives).map(({ id }) => id));
  const selectedHarnessIds = subjectIds(eventsOfType(events, "harness.selected"));
  const activatedSkillIds = subjectIds(eventsOfType(events, "skill.activated"));
  const connectedServerIds = subjectIds(eventsOfType(events, "mcp.server_connected"));
  const usedPrimitiveEvents = eventsOfType(events, "mcp.tool_selected", "mcp.tool_called", "mcp.resource_read", "mcp.prompt_used");
  const usedPrimitiveIds = subjectIds(usedPrimitiveEvents);
  const findings: EvaluationFinding[] = [];

  const checks: readonly [string, string, readonly string[], ReadonlySet<string>, ReadonlySet<string>][] = [
    ["harness", "harness", expected.harnessIds, fixtureHarnessIds, selectedHarnessIds],
    ["skill", "skill", expected.skillIds, fixtureSkillIds, activatedSkillIds],
    ["mcp_server", "MCP server", expected.mcpServerIds, fixtureServerIds, connectedServerIds],
    ["mcp_primitive", "MCP primitive", expected.mcpPrimitiveIds, fixturePrimitiveIds, usedPrimitiveIds],
  ];
  for (const [code, label, expectedIds, fixtureIds, observedIds] of checks) {
    for (const id of expectedIds) {
      if (!fixtureIds.has(id)) findings.push(missingFinding(`control.${code}_fixture_missing`, `Expected ${label} fixture is missing: ${id}`));
      else if (!observedIds.has(id)) findings.push(missingFinding(`control.${code}_not_used`, `Expected ${label} was not observed in the trace: ${id}`));
    }
    for (const id of observedIds) {
      if (!fixtureIds.has(id)) findings.push(missingFinding(`control.${code}_unmodeled`, `Trace used an unmodeled ${label}: ${id}`));
    }
  }
  if (findings.length === 0) {
    findings.push(passingFinding("control.expected_surfaces_used", "All expected harness, skill, and MCP control surfaces were modeled and used.", events.filter(({ subjectId }) =>
      subjectId !== undefined && [
        ...expected.harnessIds,
        ...expected.skillIds,
        ...expected.mcpServerIds,
        ...expected.mcpPrimitiveIds,
      ].includes(subjectId))));
  }
  return result("control-surface-quality", findings);
}

function evaluateBusinessRealism(scenario: Scenario, events: readonly NormalizedTraceEvent[]): DimensionResult {
  const observedFacts = new Set(events.flatMap(({ evidence }) => {
    const facts = evidence.businessFacts;
    return Array.isArray(facts) ? facts.filter((fact): fact is string => typeof fact === "string") : [];
  }));
  const missingFacts = scenario.businessContext.requiredFacts.filter((fact) => !observedFacts.has(fact));
  const contextEvents = events.filter(({ evidence }) => Array.isArray(evidence.businessFacts));
  const findings = missingFacts.length === 0
    ? [passingFinding("business.required_context_observed", "All required automotive business facts are evidenced in the trace.", contextEvents)]
    : missingFacts.map((fact) => missingFinding("business.required_context_missing", `Required business fact is not evidenced: ${fact}`));
  return result("business-realism", findings);
}

function evaluateObservability(scenario: Scenario, events: readonly NormalizedTraceEvent[]): DimensionResult {
  const findings: EvaluationFinding[] = [];
  for (const type of scenario.evaluation.requiredTraceTypes) {
    const matching = eventsOfType(events, type);
    if (matching.length === 0) findings.push(missingFinding("observability.required_event_missing", `Required trace event is missing: ${type}`));
  }
  const withoutEvidence = events.filter(({ evidence }) => Object.keys(evidence).length === 0);
  if (withoutEvidence.length > 0) {
    findings.push({
      code: "observability.empty_evidence",
      severity: "warning",
      message: `${withoutEvidence.length} trace event(s) have no evidence payload.`,
      evidenceRefs: withoutEvidence.map(traceEvidenceRef),
    });
  }
  if (findings.length === 0) {
    findings.push(passingFinding("observability.trace_complete", "Required trace markers include actors and evidence.", events));
  }
  return result("observability", findings);
}

function evaluateGovernance(
  scenario: Scenario,
  mcpSurfaces: readonly McpSurfaceDescriptor[],
  events: readonly NormalizedTraceEvent[],
): DimensionResult {
  const findings: EvaluationFinding[] = [];
  const failedPolicy = eventsOfType(events, "policy.check_failed");
  const passedPolicy = eventsOfType(events, "policy.check_passed");
  const confirmation = eventsOfType(events, "human.confirmation_received");
  const deniedPermission = eventsOfType(events, "harness.permission_denied");
  if (failedPolicy.length > 0) findings.push(missingFinding("governance.policy_failed", "A policy check failed.", failedPolicy.map(traceEvidenceRef)));
  if (deniedPermission.length > 0) findings.push(missingFinding("governance.permission_denied", "A required harness permission was denied.", deniedPermission.map(traceEvidenceRef)));
  if (scenario.evaluation.requiresPolicyCheck) {
    findings.push(passedPolicy.length > 0
      ? passingFinding("governance.policy_passed", "The required policy check passed.", passedPolicy)
      : missingFinding("governance.policy_missing", "The scenario requires a passing policy check."));
  }
  if (scenario.evaluation.requiresHumanConfirmation) {
    findings.push(confirmation.length > 0
      ? passingFinding("governance.confirmation_received", "The required human confirmation was received.", confirmation)
      : missingFinding("governance.confirmation_missing", "The scenario requires human confirmation."));
  }
  const governedToolIds = new Set(mcpSurfaces.flatMap(({ tools }) =>
    tools.filter(({ risk }) => risk !== "low").map(({ id }) => id)));
  const governedCalls = eventsOfType(events, "mcp.tool_called").filter(({ subjectId }) =>
    subjectId !== undefined && governedToolIds.has(subjectId));
  for (const call of governedCalls) {
    if (scenario.evaluation.requiresPolicyCheck && !passedPolicy.some(({ position }) => position < call.position)) {
      findings.push(missingFinding(
        "governance.policy_too_late",
        `A passing policy check was not recorded before governed tool call: ${call.subjectId}`,
        [traceEvidenceRef(call)],
      ));
    }
    if (scenario.evaluation.requiresHumanConfirmation && !confirmation.some(({ position }) => position < call.position)) {
      findings.push(missingFinding(
        "governance.confirmation_too_late",
        `Human confirmation was not recorded before governed tool call: ${call.subjectId}`,
        [traceEvidenceRef(call)],
      ));
    }
  }
  if (findings.length === 0) {
    findings.push(passingFinding("governance.no_required_gates", "No governance gates were required or failed.", []));
  }
  return result("governance", findings);
}

export function evaluateBenchmark(input: BenchmarkInput): BenchmarkEvaluation {
  const validationFindings = [
    ...validateScenario(input.scenario).findings,
    ...input.harnesses.flatMap((harness) => validateHarness(harness).findings),
    ...input.skills.flatMap((skill) => validateSkill(skill).findings),
    ...input.mcpSurfaces.flatMap((surface) => validateMcpSurface(surface).findings),
    ...validateTrace(input.trace).findings,
  ];
  const normalized = normalizeTrace(input.trace);
  const allValidationFindings = [...validationFindings, ...normalized.findings.filter((finding) =>
    !validationFindings.some(({ code, path }) => code === finding.code && path === finding.path))];

  return {
    scenarioId: input.scenario.id,
    valid: allValidationFindings.every(({ severity }) => severity !== "error"),
    validationFindings: allValidationFindings,
    dimensions: [
      evaluateIntent(input.scenario, normalized.events),
      evaluateControlSurfaces(input, normalized.events),
      evaluateBusinessRealism(input.scenario, normalized.events),
      evaluateObservability(input.scenario, normalized.events),
      evaluateGovernance(input.scenario, input.mcpSurfaces, normalized.events),
    ],
  };
}
