from __future__ import annotations

from collections.abc import Sequence
from typing import Literal, NotRequired, TypeAlias, TypedDict, TypeGuard, cast, get_args

from .domain import EvidencePayload, ValidationFinding

AgenticEventType: TypeAlias = Literal[
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
]

AGENTIC_EVENT_TYPES: tuple[AgenticEventType, ...] = get_args(AgenticEventType)

class RawTraceEvent(TypedDict):
    type: str
    sequence: NotRequired[int | float]
    timestamp: NotRequired[str]
    actorId: NotRequired[str]
    subjectId: NotRequired[str]
    evidence: NotRequired[EvidencePayload]


class NormalizedTraceEvent(TypedDict):
    type: AgenticEventType
    position: int
    timestamp: NotRequired[str]
    actorId: str
    subjectId: NotRequired[str]
    evidence: EvidencePayload


class TraceNormalizationResult(TypedDict):
    events: Sequence[NormalizedTraceEvent]
    findings: Sequence[ValidationFinding]


def is_agentic_event_type(value: str) -> TypeGuard[AgenticEventType]:
    return value in AGENTIC_EVENT_TYPES


def trace_evidence_ref(event: NormalizedTraceEvent) -> str:
    return f"trace:{event['position']}"


def _sequence_key(indexed: tuple[int, RawTraceEvent]) -> tuple[bool, int | float, int]:
    # Numbered events first in numeric order, then unsequenced events; ties keep input order.
    input_index, event = indexed
    sequence = event.get("sequence")
    return (sequence is None, 0 if sequence is None else sequence, input_index)


def normalize_trace(trace: Sequence[RawTraceEvent]) -> TraceNormalizationResult:
    findings: list[ValidationFinding] = []
    ordered = sorted(enumerate(trace), key=_sequence_key)

    events: list[NormalizedTraceEvent] = []
    for input_index, event in ordered:
        event_type = event["type"]
        if not is_agentic_event_type(event_type):
            findings.append({
                "code": "trace.unknown_event_type",
                "severity": "error",
                "path": f"trace[{input_index}].type",
                "message": f"Unknown agentic event type: {event_type or '<empty>'}",
            })
            continue
        actor_id = event.get("actorId")
        if actor_id is None or not actor_id.strip():
            findings.append({
                "code": "trace.missing_actor",
                "severity": "error",
                "path": f"trace[{input_index}].actorId",
                "message": "Trace events require an actor identifier.",
            })
            continue

        normalized: dict[str, object] = {"type": event_type, "position": len(events) + 1}
        if "timestamp" in event:
            normalized["timestamp"] = event["timestamp"]
        normalized["actorId"] = actor_id
        if "subjectId" in event:
            normalized["subjectId"] = event["subjectId"]
        evidence = event.get("evidence")
        normalized["evidence"] = {} if evidence is None else evidence
        events.append(cast(NormalizedTraceEvent, normalized))

    return {"events": events, "findings": findings}
