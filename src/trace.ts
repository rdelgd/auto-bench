import type { EvidencePayload, ValidationFinding } from "./domain.js";

export const agenticEventTypes = [
  "intent.submitted",
  "lasm.version_selected",
  "lasm.projection_loaded",
  "lasm.entry_consulted",
  "lasm.evaluation_requested",
  "lasm.evaluation_passed",
  "lasm.evaluation_failed",
  "lasm.divergence_detected",
  "lasm.failure_attributed",
  "state.observed",
  "state.transition_proposed",
  "state.transition_committed",
  "state.transition_rejected",
  "agent.role_selected",
  "harness.selected",
  "harness.configured",
  "harness.context_loaded",
  "harness.permission_requested",
  "harness.permission_granted",
  "harness.permission_denied",
  "skill.discovered",
  "skill.activated",
  "skill.reference_loaded",
  "mcp.server_connected",
  "mcp.primitives_listed",
  "mcp.tool_selected",
  "mcp.tool_called",
  "mcp.resource_read",
  "mcp.prompt_used",
  "policy.check_requested",
  "policy.check_passed",
  "policy.check_failed",
  "human.confirmation_requested",
  "human.confirmation_received",
  "handoff.created",
  "outcome.observed",
  "outcome.validated",
  "evidence.linked",
  "task.completed",
  "task.failed",
  "intent.fidelity_assessed",
  "reality.validation_assessed",
] as const;

export type AgenticEventType = (typeof agenticEventTypes)[number];

export interface RawTraceEvent {
  readonly type: string;
  readonly sequence?: number;
  readonly timestamp?: string;
  readonly actorId?: string;
  readonly subjectId?: string;
  readonly evidence?: EvidencePayload;
}

export interface NormalizedTraceEvent {
  readonly type: AgenticEventType;
  readonly position: number;
  readonly timestamp?: string;
  readonly actorId: string;
  readonly subjectId?: string;
  readonly evidence: EvidencePayload;
}

export interface TraceNormalizationResult {
  readonly events: readonly NormalizedTraceEvent[];
  readonly findings: readonly ValidationFinding[];
}

export function isAgenticEventType(value: string): value is AgenticEventType {
  return (agenticEventTypes as readonly string[]).includes(value);
}

export function traceEvidenceRef(event: NormalizedTraceEvent): string {
  return `trace:${event.position}`;
}

export function normalizeTrace(trace: readonly RawTraceEvent[]): TraceNormalizationResult {
  const findings: ValidationFinding[] = [];
  const ordered = trace
    .map((event, inputIndex) => ({ event, inputIndex }))
    .sort((left, right) => {
      const leftSequence = left.event.sequence ?? Number.MAX_SAFE_INTEGER;
      const rightSequence = right.event.sequence ?? Number.MAX_SAFE_INTEGER;
      return leftSequence - rightSequence || left.inputIndex - right.inputIndex;
    });

  const events: NormalizedTraceEvent[] = [];
  for (const { event, inputIndex } of ordered) {
    if (!isAgenticEventType(event.type)) {
      findings.push({
        code: "trace.unknown_event_type",
        severity: "error",
        path: `trace[${inputIndex}].type`,
        message: `Unknown agentic event type: ${event.type || "<empty>"}`,
      });
      continue;
    }
    if (!event.actorId?.trim()) {
      findings.push({
        code: "trace.missing_actor",
        severity: "error",
        path: `trace[${inputIndex}].actorId`,
        message: "Trace events require an actor identifier.",
      });
      continue;
    }

    events.push({
      type: event.type,
      position: events.length + 1,
      ...(event.timestamp === undefined ? {} : { timestamp: event.timestamp }),
      actorId: event.actorId,
      ...(event.subjectId === undefined ? {} : { subjectId: event.subjectId }),
      evidence: event.evidence ?? {},
    });
  }

  return { events, findings };
}
