import type { ConformanceCase } from "./conformance.js";
import type { ValidationFinding } from "./domain.js";
import type { LasmProjectionReferences } from "./lasm.js";
import { mcpPrimitives, type McpSurfaceDescriptor } from "./mcp.js";
import type { Scenario } from "./scenario.js";
import { normalizeTrace, traceEvidenceRef, type AgenticEventType, type NormalizedTraceEvent } from "./trace.js";
import { validateConformanceCase, validateLogicalAssembly } from "./validate.js";

export type EvaluationDimension =
  | "intent-fidelity"
  | "semantic-fidelity"
  | "reality-model-validity"
  | "state-and-outcome-validity"
  | "control-surface-quality"
  | "reality-coverage"
  | "evidence-and-attribution"
  | "governance";
export type EvaluationStatus = "pass" | "warning" | "fail";
export type EvaluationFindingSeverity = "info" | "warning" | "error";
export type DivergenceSource =
  | "reality-model"
  | "projection"
  | "control-surface"
  | "agent-conduct"
  | "external-system"
  | "insufficient-evidence";

export interface EvaluationFinding {
  readonly code: string;
  readonly severity: EvaluationFindingSeverity;
  readonly message: string;
  readonly evidenceRefs: readonly string[];
  readonly assemblyEntryIds: readonly string[];
  readonly transitionIds: readonly string[];
  readonly outcomeIds: readonly string[];
  readonly attribution?: DivergenceSource;
}

export interface DimensionResult {
  readonly dimension: EvaluationDimension;
  readonly status: EvaluationStatus;
  readonly findings: readonly EvaluationFinding[];
  readonly evidenceRefs: readonly string[];
}

export interface ConformanceEvaluation {
  readonly assemblyId: string;
  readonly assemblyVersion: string;
  readonly scenarioId: string;
  readonly valid: boolean;
  readonly conformant: boolean;
  readonly validationFindings: readonly ValidationFinding[];
  readonly dimensions: readonly DimensionResult[];
}

interface FindingDetails {
  readonly evidenceRefs?: readonly string[];
  readonly assemblyEntryIds?: readonly string[];
  readonly transitionIds?: readonly string[];
  readonly outcomeIds?: readonly string[];
  readonly attribution?: DivergenceSource;
}

function eventsOfType(events: readonly NormalizedTraceEvent[], ...types: AgenticEventType[]): readonly NormalizedTraceEvent[] {
  return events.filter(({ type }) => types.includes(type));
}

function subjectIds(events: readonly NormalizedTraceEvent[]): ReadonlySet<string> {
  return new Set(events.flatMap(({ subjectId }) => subjectId === undefined ? [] : [subjectId]));
}

function unique(values: readonly string[]): readonly string[] {
  return [...new Set(values)];
}

function dimensionEvidenceRefs(findings: readonly EvaluationFinding[]): readonly string[] {
  return unique(findings.flatMap((finding) => finding.evidenceRefs));
}

function result(dimension: EvaluationDimension, findings: readonly EvaluationFinding[]): DimensionResult {
  const status: EvaluationStatus = findings.some(({ severity }) => severity === "error")
    ? "fail"
    : findings.some(({ severity }) => severity === "warning")
      ? "warning"
      : "pass";
  return { dimension, status, findings, evidenceRefs: dimensionEvidenceRefs(findings) };
}

function finding(
  code: string,
  severity: EvaluationFindingSeverity,
  message: string,
  details: FindingDetails = {},
): EvaluationFinding {
  return {
    code,
    severity,
    message,
    evidenceRefs: details.evidenceRefs ?? [],
    assemblyEntryIds: details.assemblyEntryIds ?? [],
    transitionIds: details.transitionIds ?? [],
    outcomeIds: details.outcomeIds ?? [],
    ...(details.attribution === undefined ? {} : { attribution: details.attribution }),
  };
}

function passingFinding(code: string, message: string, events: readonly NormalizedTraceEvent[], details: FindingDetails = {}): EvaluationFinding {
  return finding(code, "info", message, { ...details, evidenceRefs: events.map(traceEvidenceRef) });
}

function projectionReferences(input: ConformanceCase): readonly LasmProjectionReferences[] {
  const harnessReferences = input.harnesses.flatMap((harness) => [
    harness.projection,
    ...harness.contextSurfaces.map(({ projection }) => projection),
    harness.permissionModel.projection,
    harness.approvalFlow.projection,
    ...harness.handoffBoundaries.map(({ projection }) => projection),
  ]);
  const skillReferences = input.skills.map(({ projection }) => projection);
  const mcpReferences = input.mcpSurfaces.flatMap((surface) => [
    surface.projection,
    ...mcpPrimitives(surface).map(({ projection }) => projection),
  ]);
  return [...harnessReferences, ...skillReferences, ...mcpReferences].filter(
    (projection): projection is LasmProjectionReferences => projection !== undefined,
  );
}

function evaluateIntent(scenario: Scenario, events: readonly NormalizedTraceEvent[]): DimensionResult {
  const submitted = eventsOfType(events, "intent.submitted");
  const outcomes = eventsOfType(events, "task.completed", "task.failed");
  const preserved = submitted.filter(({ evidence }) => evidence.goal === scenario.intent.explicitGoal);
  const findings: EvaluationFinding[] = [];
  findings.push(preserved.length > 0
    ? passingFinding("intent.explicit_goal_observed", "The submitted intent matches the scenario's explicit goal.", preserved)
    : finding("intent.explicit_goal_missing", "error", "The trace does not preserve the scenario's explicit goal.", {
      evidenceRefs: submitted.map(traceEvidenceRef),
      attribution: "agent-conduct",
    }));
  findings.push(outcomes.some(({ type }) => type === "task.completed")
    ? passingFinding("intent.outcome_completed", "The trace records a completed business outcome.", outcomes)
    : finding("intent.outcome_incomplete", "error", "The trace does not record successful task completion.", {
      evidenceRefs: outcomes.map(traceEvidenceRef),
      attribution: "agent-conduct",
    }));
  return result("intent-fidelity", findings);
}

function evaluateSemanticFidelity(input: ConformanceCase, events: readonly NormalizedTraceEvent[]): DimensionResult {
  const relevantEntryIds = input.scenario.reality.assemblyEntryIds;
  const consultedEvents = eventsOfType(events, "lasm.entry_consulted");
  const consultedIds = subjectIds(consultedEvents);
  const divergenceEvents = eventsOfType(events, "lasm.divergence_detected");
  const findings: EvaluationFinding[] = [];

  for (const id of relevantEntryIds) {
    const matching = consultedEvents.filter(({ subjectId }) => subjectId === id);
    findings.push(consultedIds.has(id)
      ? passingFinding("semantic.entry_consulted", `Relevant assembly entry was consulted: ${id}`, matching, { assemblyEntryIds: [id] })
      : finding("semantic.entry_not_consulted", "error", `Relevant assembly entry was not evidenced as consulted: ${id}`, {
        assemblyEntryIds: [id],
        attribution: "insufficient-evidence",
      }));
  }
  for (const divergence of divergenceEvents) {
    findings.push(finding("semantic.divergence_detected", "error", "The episode records semantic divergence.", {
      evidenceRefs: [traceEvidenceRef(divergence)],
      assemblyEntryIds: divergence.subjectId === undefined ? [] : [divergence.subjectId],
      attribution: "projection",
    }));
  }
  return result("semantic-fidelity", findings);
}

function evaluateRealityModel(input: ConformanceCase, events: readonly NormalizedTraceEvent[]): DimensionResult {
  const findings: EvaluationFinding[] = [];
  const assemblyValidation = validateLogicalAssembly(input.assembly);
  for (const validation of assemblyValidation.findings) {
    findings.push(finding("reality.invalid_assembly", validation.severity === "error" ? "error" : "warning", validation.message, {
      attribution: "reality-model",
    }));
  }
  for (const source of input.assembly.provenance) {
    if (source.status === "stale") {
      findings.push(finding("reality.stale_source", "error", `Assembly provenance is stale: ${source.id}`, { attribution: "reality-model" }));
    } else if (source.status === "disputed") {
      findings.push(finding("reality.disputed_source", "warning", `Assembly provenance is disputed: ${source.id}`, { attribution: "reality-model" }));
    }
  }
  const selected = eventsOfType(events, "lasm.version_selected").filter(({ subjectId, evidence }) =>
    subjectId === input.assembly.id && evidence.version === input.assembly.version);
  findings.push(selected.length > 0
    ? passingFinding("reality.version_selected", "The episode identifies the governing assembly and version.", selected)
    : finding("reality.version_not_selected", "error", "The trace does not identify the governing assembly version.", {
      attribution: "insufficient-evidence",
    }));
  if (findings.length === 1 && selected.length > 0) {
    findings.push(finding("reality.sources_current", "info", "All assembly provenance sources are current."));
  }
  return result("reality-model-validity", findings);
}

function evaluateStateAndOutcomes(input: ConformanceCase, events: readonly NormalizedTraceEvent[]): DimensionResult {
  const findings: EvaluationFinding[] = [];
  const observedIds = subjectIds(eventsOfType(events, "state.observed"));
  for (const observation of input.observations) {
    findings.push(observedIds.has(observation.id)
      ? passingFinding("state.observation_evidenced", `Actor observation was evidenced: ${observation.id}`, events.filter(({ type, subjectId }) => type === "state.observed" && subjectId === observation.id))
      : finding("state.observation_missing", "error", `Required actor observation is missing: ${observation.id}`, { attribution: "insufficient-evidence" }));
  }

  const committed = eventsOfType(events, "state.transition_committed");
  const committedIds = subjectIds(committed);
  for (const transition of input.transitions) {
    const matching = committed.filter(({ subjectId }) => subjectId === transition.id);
    if (transition.disposition === "prohibited" && committedIds.has(transition.id)) {
      findings.push(finding("state.prohibited_transition_committed", "error", `A prohibited state transition was committed: ${transition.id}`, {
        evidenceRefs: matching.map(traceEvidenceRef),
        transitionIds: [transition.id],
        attribution: "agent-conduct",
      }));
    } else if (transition.disposition === "permitted" && transition.required && !committedIds.has(transition.id)) {
      findings.push(finding("state.required_transition_missing", "error", `A required state transition was not committed: ${transition.id}`, {
        transitionIds: [transition.id],
        attribution: "insufficient-evidence",
      }));
    } else {
      findings.push(passingFinding("state.transition_conformant", `State transition evidence conforms: ${transition.id}`, matching, { transitionIds: [transition.id] }));
    }
  }

  const observedOutcomes = eventsOfType(events, "outcome.observed");
  const validatedOutcomes = eventsOfType(events, "outcome.validated");
  const observedOutcomeIds = subjectIds(observedOutcomes);
  const validatedOutcomeIds = subjectIds(validatedOutcomes);
  for (const outcome of input.outcomes) {
    const matching = [...observedOutcomes, ...validatedOutcomes].filter(({ subjectId }) => subjectId === outcome.id);
    if (outcome.disposition === "prohibited" && observedOutcomeIds.has(outcome.id)) {
      findings.push(finding("outcome.prohibited_observed", "error", `A prohibited outcome was observed: ${outcome.id}`, {
        evidenceRefs: matching.map(traceEvidenceRef),
        outcomeIds: [outcome.id],
        attribution: "agent-conduct",
      }));
    } else if (outcome.disposition === "acceptable" && outcome.required && !validatedOutcomeIds.has(outcome.id)) {
      findings.push(finding("outcome.required_not_validated", "error", `A required acceptable outcome was not validated: ${outcome.id}`, {
        outcomeIds: [outcome.id],
        attribution: "insufficient-evidence",
      }));
    } else {
      findings.push(passingFinding("outcome.expectation_satisfied", `Outcome evidence conforms: ${outcome.id}`, matching, { outcomeIds: [outcome.id] }));
    }
  }
  return result("state-and-outcome-validity", findings);
}

function evaluateControlSurfaces(input: ConformanceCase, events: readonly NormalizedTraceEvent[]): DimensionResult {
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
      if (!fixtureIds.has(id)) {
        findings.push(finding(`control.${code}_fixture_missing`, "error", `Expected ${label} fixture is missing: ${id}`, { attribution: "control-surface" }));
      } else if (!observedIds.has(id)) {
        findings.push(finding(`control.${code}_not_used`, "error", `Expected ${label} was not observed in the trace: ${id}`, { attribution: "agent-conduct" }));
      }
    }
    for (const id of observedIds) {
      if (!fixtureIds.has(id)) findings.push(finding(`control.${code}_unmodeled`, "error", `Trace used an unmodeled ${label}: ${id}`, { attribution: "control-surface" }));
    }
  }
  if (findings.length === 0) {
    findings.push(passingFinding("control.expected_surfaces_used", "All expected Lasm projections and control surfaces were modeled and used.", events.filter(({ subjectId }) =>
      subjectId !== undefined && [
        ...expected.harnessIds,
        ...expected.skillIds,
        ...expected.mcpServerIds,
        ...expected.mcpPrimitiveIds,
      ].includes(subjectId))));
  }
  return result("control-surface-quality", findings);
}

function evaluateRealityCoverage(input: ConformanceCase, events: readonly NormalizedTraceEvent[]): DimensionResult {
  const findings: EvaluationFinding[] = [];
  const projectedEntryIds = new Set(projectionReferences(input).flatMap(({ assemblyEntryIds }) => assemblyEntryIds));
  for (const id of input.scenario.reality.assemblyEntryIds) {
    if (!projectedEntryIds.has(id)) {
      findings.push(finding("coverage.assembly_entry_not_projected", "error", `Relevant assembly entry is absent from agent-facing projections: ${id}`, {
        assemblyEntryIds: [id],
        attribution: "projection",
      }));
    }
  }

  const observedFacts = new Set(events.flatMap(({ evidence }) => {
    const facts = evidence.businessFacts;
    return Array.isArray(facts) ? facts.filter((fact): fact is string => typeof fact === "string") : [];
  }));
  for (const fact of input.scenario.businessContext.requiredFacts) {
    if (!observedFacts.has(fact)) {
      findings.push(finding("coverage.required_fact_missing", "error", `Required operational fact is not evidenced: ${fact}`, { attribution: "insufficient-evidence" }));
    }
  }
  if (findings.length === 0) {
    findings.push(passingFinding("coverage.relevant_reality_covered", "Relevant assembly entries and operational facts are covered.", events.filter(({ evidence }) => Array.isArray(evidence.businessFacts)), {
      assemblyEntryIds: input.scenario.reality.assemblyEntryIds,
    }));
  }
  return result("reality-coverage", findings);
}

function evaluateEvidenceAndAttribution(scenario: Scenario, events: readonly NormalizedTraceEvent[]): DimensionResult {
  const findings: EvaluationFinding[] = [];
  for (const type of scenario.evaluation.requiredTraceTypes) {
    const matching = eventsOfType(events, type);
    if (matching.length === 0) {
      findings.push(finding("evidence.required_event_missing", "error", `Required evidence event is missing: ${type}`, { attribution: "insufficient-evidence" }));
    }
  }
  const withoutEvidence = events.filter(({ evidence }) => Object.keys(evidence).length === 0);
  if (withoutEvidence.length > 0) {
    findings.push(finding("evidence.empty_payload", "warning", `${withoutEvidence.length} event(s) have no evidence payload.`, {
      evidenceRefs: withoutEvidence.map(traceEvidenceRef),
      attribution: "insufficient-evidence",
    }));
  }
  const linked = eventsOfType(events, "evidence.linked");
  if (linked.length === 0) {
    findings.push(finding("evidence.links_missing", "error", "The episode contains no explicit evidence link.", { attribution: "insufficient-evidence" }));
  }
  const divergences = eventsOfType(events, "lasm.divergence_detected", "lasm.evaluation_failed");
  const attributed = eventsOfType(events, "lasm.failure_attributed");
  for (const divergence of divergences) {
    const hasAttribution = attributed.some(({ subjectId }) => subjectId === divergence.subjectId);
    if (!hasAttribution) {
      findings.push(finding("attribution.failure_unattributed", "error", `Failure lacks attribution: ${divergence.subjectId ?? "<unknown>"}`, {
        evidenceRefs: [traceEvidenceRef(divergence)],
        assemblyEntryIds: divergence.subjectId === undefined ? [] : [divergence.subjectId],
        attribution: "insufficient-evidence",
      }));
    }
  }
  if (findings.length === 0) {
    findings.push(passingFinding("evidence.episode_attributable", "Required evidence is present and failures are attributable.", linked));
  }
  return result("evidence-and-attribution", findings);
}

function evaluateGovernance(
  scenario: Scenario,
  mcpSurfaces: readonly McpSurfaceDescriptor[],
  events: readonly NormalizedTraceEvent[],
): DimensionResult {
  const findings: EvaluationFinding[] = [];
  const failedPolicy = eventsOfType(events, "policy.check_failed", "lasm.evaluation_failed");
  const passedPolicy = eventsOfType(events, "policy.check_passed", "lasm.evaluation_passed");
  const confirmation = eventsOfType(events, "human.confirmation_received");
  const deniedPermission = eventsOfType(events, "harness.permission_denied");
  if (failedPolicy.length > 0) findings.push(finding("governance.policy_failed", "error", "A policy or runtime Lasm evaluation failed.", { evidenceRefs: failedPolicy.map(traceEvidenceRef), attribution: "agent-conduct" }));
  if (deniedPermission.length > 0) findings.push(finding("governance.permission_denied", "error", "A required harness permission was denied.", { evidenceRefs: deniedPermission.map(traceEvidenceRef), attribution: "control-surface" }));
  if (scenario.evaluation.requiresPolicyCheck) {
    findings.push(passedPolicy.length > 0
      ? passingFinding("governance.policy_passed", "The required policy or Lasm runtime evaluation passed.", passedPolicy)
      : finding("governance.policy_missing", "error", "The scenario requires a passing policy or Lasm runtime evaluation.", { attribution: "insufficient-evidence" }));
  }
  if (scenario.evaluation.requiresHumanConfirmation) {
    findings.push(confirmation.length > 0
      ? passingFinding("governance.confirmation_received", "The required human confirmation was received.", confirmation)
      : finding("governance.confirmation_missing", "error", "The scenario requires human confirmation.", { attribution: "agent-conduct" }));
  }
  const governedToolIds = new Set(mcpSurfaces.flatMap(({ tools }) =>
    tools.filter(({ risk }) => risk !== "low").map(({ id }) => id)));
  const governedCalls = eventsOfType(events, "mcp.tool_called").filter(({ subjectId }) =>
    subjectId !== undefined && governedToolIds.has(subjectId));
  for (const call of governedCalls) {
    if (scenario.evaluation.requiresPolicyCheck && !passedPolicy.some(({ position }) => position < call.position)) {
      findings.push(finding("governance.policy_too_late", "error", `A passing policy check was not recorded before governed tool call: ${call.subjectId}`, {
        evidenceRefs: [traceEvidenceRef(call)],
        attribution: "agent-conduct",
      }));
    }
    if (scenario.evaluation.requiresHumanConfirmation && !confirmation.some(({ position }) => position < call.position)) {
      findings.push(finding("governance.confirmation_too_late", "error", `Human confirmation was not recorded before governed tool call: ${call.subjectId}`, {
        evidenceRefs: [traceEvidenceRef(call)],
        attribution: "agent-conduct",
      }));
    }
  }
  if (findings.length === 0) {
    findings.push(passingFinding("governance.no_required_gates", "No governance gates were required or failed.", []));
  }
  return result("governance", findings);
}

export function evaluateConformance(input: ConformanceCase): ConformanceEvaluation {
  const validation = validateConformanceCase(input);
  const normalized = normalizeTrace(input.trace);
  const validationFindings = [...validation.findings, ...normalized.findings.filter((finding) =>
    !validation.findings.some(({ code, path }) => code === finding.code && path === finding.path))];
  const dimensions = [
    evaluateIntent(input.scenario, normalized.events),
    evaluateSemanticFidelity(input, normalized.events),
    evaluateRealityModel(input, normalized.events),
    evaluateStateAndOutcomes(input, normalized.events),
    evaluateControlSurfaces(input, normalized.events),
    evaluateRealityCoverage(input, normalized.events),
    evaluateEvidenceAndAttribution(input.scenario, normalized.events),
    evaluateGovernance(input.scenario, input.mcpSurfaces, normalized.events),
  ] as const;
  const valid = validationFindings.every(({ severity }) => severity !== "error");

  return {
    assemblyId: input.assembly.id,
    assemblyVersion: input.assembly.version,
    scenarioId: input.scenario.id,
    valid,
    conformant: valid && dimensions.every(({ status }) => status !== "fail"),
    validationFindings,
    dimensions,
  };
}

export type { ConformanceCase } from "./conformance.js";
